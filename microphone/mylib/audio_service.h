#ifndef AUDIO_SERVICE_H_
#define AUDIO_SERVICE_H_
#include <zephyr/types.h>
#include <stddef.h>
#include <string.h>
#include <errno.h>
#include <zephyr/sys/printk.h>
#include <zephyr/sys/byteorder.h>
#include <zephyr/kernel.h>

#include <zephyr/bluetooth/bluetooth.h>
#include <zephyr/bluetooth/hci.h>
#include <zephyr/bluetooth/conn.h>
#include <zephyr/bluetooth/uuid.h>
#include <zephyr/bluetooth/gatt.h>
#include <zephyr/bluetooth/services/hrs.h>
#include <stdint.h>
#include <zephyr/sys/util.h>
#include <zephyr/bluetooth/byteorder.h>

/* Define UUID for Audio Service and Characteristic */
#define BT_UUID_AUDIO_VAL 0x1798
#define BT_UUID_AUDIO \
        BT_UUID_DECLARE_16(BT_UUID_AUDIO_VAL)
#define BT_UUID_AUDIO_DATA_VAL 0x1799
#define BT_UUID_AUDIO_DATA \
        BT_UUID_DECLARE_16(BT_UUID_AUDIO_DATA_VAL)

/** @brief Initialize the Audio Service. */
void audio_service_init(void);

/** @brief Initialize Bluetooth audio. */
int bluetooth_audio_init(void);

/** @brief Send a 16-bit PCM audio value. */
void audio_notify(uint16_t pcm_value);


#endif /* AUDIO_SERVICE_H_ */
