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
#include "microphone_test.h"

LOG_MODULE_REGISTER(dmic_sample);

K_MSGQ_DEFINE(recv_msgq, SLAB_SIZE, 8, 1);

// Memory stack for the audio buffer - adjust the number of MS till we reach our max RAM
/* NAME OF SLAB     BLOCK SIZE   HOW MANY BLOCKS    N-BYTE Boundary*/
K_MEM_SLAB_DEFINE_STATIC(mem_slab, PCM_BLK_SIZE_MS, NUM_MS, 4);

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
			   struct dmic_cfg *cfg)
{
	int ret;


	LOG_INF("PCM output rate: %u, channels: %u",
		cfg->streams[0].pcm_rate, cfg->channel.req_num_chan);
	
	// Configure digital microphone driver
	ret = dmic_configure(dmic_dev, cfg);
	if (ret < 0) {
		LOG_ERR("Failed to configure the driver: %d", ret);
		return ret;
	}

    void *buffer;
	size_t size;

	


    while(1) {

		// Enable the stream
		ret = dmic_trigger(dmic_dev, DMIC_TRIGGER_START);
		if (ret < 0) {
			LOG_ERR("START trigger failed: %d", ret);
			return ret;
		}


        // Read microphone data
        // Fills our entire slab (I believe)
        ret = dmic_read(dmic_dev, 0, &buffer, &size, READ_TIMEOUT);
        if (ret < 0) {
            // LOG_ERR("%d - read failed: %d", i, ret);
            return ret;
        }
		//printk("New line to take up space\n\r");
		printk("got buffer %p of %u bytes\n\r", buffer, size);
		
		printk("Here1\n\r");

        k_msgq_put(&recv_msgq, (uint16_t*)buffer, K_NO_WAIT);
		printk("Here2\n\r");
    
        k_mem_slab_free(&mem_slab, buffer);
		printk("Here3\n\r");

        //k_sleep(K_MSEC(100));
   


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
	cfg.streams[0].pcm_rate = AUDIO_FREQ;
	cfg.streams[0].block_size = 
		BLOCK_SIZE(cfg.streams[0].pcm_rate, cfg.channel.req_num_chan);

	// Start reading PCM data
    ret = do_pdm_transfer(dmic_dev, &cfg);
    if (ret < 0) {
        return 0;
    }

	LOG_INF("Exiting");
	return 0;
}
