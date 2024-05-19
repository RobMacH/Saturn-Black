/*
 * Copyright (c) 2021 Nordic Semiconductor ASA
 *
 * SPDX-License-Identifier: Apache-2.0
 */
#ifndef MICROPHONE_TEST_H_
#define MICROPHONE_TEST_H_

#include <zephyr/kernel.h>
#include <zephyr/audio/dmic.h>

#include <zephyr/logging/log.h>
#define MSG_SIZE 16

// Sampling Frequency
#define AUDIO_FREQ          16000
// Samples per ms
#define SAMPLE_WIDTH        AUDIO_FREQ / 1000 

#define SAMPLE_BIT_WIDTH 	16
// Bytes per samples
#define BYTES_PER_SAMPLE    sizeof(int16_t)
// Block size for 1ms of data (each sample is int16_t)
#define PCM_BLK_SIZE_MS     ((SAMPLE_WIDTH) * BYTES_PER_SAMPLE) // 16 * 2 = 32B
// How many MS of audio we can record
#define NUM_MS              100
// Total slab/buffer size in Bytes
#define SLAB_SIZE           PCM_BLK_SIZE_MS * NUM_MS 
// Number of spaces in a uint16 array (buffer)
#define BUF_SIZE            SLAB_SIZE / BYTES_PER_SAMPLE 

/* Milliseconds to wait for a block to be read. */
#define READ_TIMEOUT     5000

/* Size of a block for 100 ms of audio data. */
#define BLOCK_SIZE(_sample_rate, _number_of_channels) \
	(BYTES_PER_SAMPLE * (_sample_rate / 10) * _number_of_channels)


int do_pdm_transfer(const struct device *dmic_dev,
			   struct dmic_cfg *cfg);
int mic_init(void);

#endif