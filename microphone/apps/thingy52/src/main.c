/*
 * Copyright (c) 2021 Nordic Semiconductor ASA
 *
 * SPDX-License-Identifier: Apache-2.0
 */

#include <zephyr/kernel.h>
#include <zephyr/audio/dmic.h>

#include <zephyr/bluetooth/bluetooth.h>
#include <zephyr/bluetooth/conn.h>
#include <zephyr/bluetooth/gatt.h>

#include <zephyr/logging/log.h>
#include "../../../mylib/microphone.h"
#include <stdint.h>
#include "../../../mylib/bluetooth_audio.h"
#include <zephyr/sys/printk.h>

// Thread definitions
#define BLUETOOTH_PRIORITY 3
#define BLUETOOTH_STACK 7000
#define MIC_PRIORITY 4
#define MIC_STACK 4096

int main(void)
{

	//mic_init();
	//bluetooth_hr_init();
	return 0;
}

// Thread definitions
K_THREAD_DEFINE(bluetooth_hr_tid, BLUETOOTH_STACK, bluetooth_audio_init, NULL, NULL, NULL, BLUETOOTH_PRIORITY, 0, 0);
K_THREAD_DEFINE(mic_tid, MIC_STACK, mic_init, NULL, NULL, NULL, MIC_PRIORITY, 0, 0);

