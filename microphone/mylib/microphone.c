/*
 * Copyright (c) 2021 Nordic Semiconductor ASA
 *
 * SPDX-License-Identifier: Apache-2.0
 */

#include <zephyr/kernel.h>
#include <zephyr/audio/dmic.h>
#include <zephyr/logging/log.h>
#include <zephyr/drivers/gpio.h>
#include <zephyr/init.h>
#include "microphone.h"

LOG_MODULE_REGISTER(dmic_sample);

K_SEM_DEFINE(mic_sem, 1, 1);

// Message queue for the 16 bit PCM data
K_MSGQ_DEFINE(recv_msgq, MSG_SIZE, 1600*4, 1);

// Memory stack for the audio buffer
K_MEM_SLAB_DEFINE_STATIC(mem_slab, MAX_BLOCK_SIZE, BLOCK_COUNT, 4);

/* PDM transfer function to configure the microphone and 
*  send data to the message queue for advertising
*/

static const struct gpio_dt_spec mic_gpio = GPIO_DT_SPEC_GET(DT_NODELABEL(mic_pwr), enable_gpios);

static int pwr_ctrl_init(void)
{
	int ret;

	if (!gpio_is_ready_dt(&mic_gpio)) {
		return -ENODEV;
	}	

	ret = gpio_pin_configure_dt(&mic_gpio, GPIO_OUTPUT_HIGH);
	if (ret < 0) {
		return ret;
	}

	k_sleep(K_MSEC(1)); /* Wait for the rail to come up and stabilize */

	return 0;
}


// #if CONFIG_SENSOR_INIT_PRIORITY <= CONFIG_BOARD_CCS_VDD_PWR_CTRL_INIT_PRIORITY
// #error BOARD_CCS_VDD_PWR_CTRL_INIT_PRIORITY must be lower than SENSOR_INIT_PRIORITY
// #endif

// SYS_INIT(pwr_ctrl_init, POST_KERNEL,
// 	 CONFIG_BOARD_CCS_VDD_PWR_CTRL_INIT_PRIORITY);

int do_pdm_transfer(const struct device *dmic_dev,
			   struct dmic_cfg *cfg,
			   size_t block_count)
{
	int ret;
	char msg[MSG_SIZE];

	LOG_INF("PCM output rate: %u, channels: %u",
		cfg->streams[0].pcm_rate, cfg->channel.req_num_chan);
	
	// Configure digital microphone driver
	ret = dmic_configure(dmic_dev, cfg);
	if (ret < 0) {
		LOG_ERR("Failed to configure the driver: %d", ret);
		return ret;
	}

	uint16_t sample = 0;
	ret = dmic_trigger(dmic_dev, DMIC_TRIGGER_START);
		if (ret < 0) {
			LOG_ERR("START trigger failed: %d", ret);
			return ret;
		}
	
	//k_sleep(K_MSEC(5000));
	int size_count = 0;
	int count = 0;

    while(1){

		count ++;
		if (count == 25) {
			printk("Size after 10 sec: %u\n", size_count);
		}

		if (k_sem_take(&mic_sem, K_MSEC(50)) != 0) {

			printk("Input data not available!\n");
			
		} else {

			for (int i = 0; i < block_count; ++i) {

				void *buffer;
				uint32_t size;
				// Read microphone data
				ret = dmic_read(dmic_dev, 0, &buffer, &size, READ_TIMEOUT);
				if (ret < 0) {
					//LOG_ERR("%d - read failed: %d", i, ret);
					return ret;
				}

				size_count += size;

				uint16_t *audio_data = (uint16_t *)buffer;
				
				for(int j = 0; j < 1600; j+=1){
					//printk("%d \n", audio_data[j]);
					sample = audio_data[j];
					//printk("%u\n", sample);
					k_msgq_put(&recv_msgq, &sample, K_NO_WAIT);
				}

				k_mem_slab_free(&mem_slab, buffer);
			}

        }
		printk("Microphone done! heres the sem\n");
		k_sem_give(&mic_sem);
    }
	ret = dmic_trigger(dmic_dev, DMIC_TRIGGER_STOP);
	if (ret < 0) {
		LOG_ERR("STOP trigger failed: %d", ret);
		return ret;
	}


	return ret;
}

/* Initates the microhpone driver with required config values*/
int mic_init(void)
{
	pwr_ctrl_init();
	const struct device *const dmic_dev = DEVICE_DT_GET(DT_NODELABEL(dmic_dev));
	int ret;

	LOG_INF("DMIC sample");
	
	// Check device is connectable
	if (!device_is_ready(dmic_dev)) {
		LOG_ERR("%s is not ready", dmic_dev->name);
		return 0;
	}

	struct pcm_stream_cfg stream = {
		.pcm_width = SAMPLE_BIT_WIDTH,
		.mem_slab  = &mem_slab,
	};
	struct dmic_cfg cfg = {
		.io = {
			/* These fields can be used to limit the PDM clock
			 * configurations that the driver is allowed to use
			 * to those supported by the microphone.
			 */
			.min_pdm_clk_freq = 1000000,
			.max_pdm_clk_freq = 3500000,
			.min_pdm_clk_dc   = 40,
			.max_pdm_clk_dc   = 60,
		},
		.streams = &stream,
		.channel = {
			.req_num_streams = 1,
		},
	};

	// Channel configuration
	cfg.channel.req_num_chan = 1;
	cfg.channel.req_chan_map_lo =
		dmic_build_channel_map(0, 0, PDM_CHAN_LEFT);
	cfg.streams[0].pcm_rate = MAX_SAMPLE_RATE;
	cfg.streams[0].block_size =
		BLOCK_SIZE(cfg.streams[0].pcm_rate, cfg.channel.req_num_chan);

	// Start reading PCM data
    ret = do_pdm_transfer(dmic_dev, &cfg, BLOCK_COUNT);
    if (ret < 0) {
        return 0;
    }

	LOG_INF("Exiting");
	return 0;
}
