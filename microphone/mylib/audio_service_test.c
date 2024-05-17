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
#include "audio_service.h"
// #include "microphone_test.h"
#include "microphone.h"
#include <zephyr/sys/util.h>
#include <zephyr/bluetooth/byteorder.h>

// Queue to be accessed outside this module
extern struct k_msgq recv_msgq;

// Audio value and update flag 
static uint16_t audio_pcm_value = 0;
static uint8_t audio_update = 0;

// Function for CCC value, required but not necessary for our functionality
static void audio_ccc_cfg_changed(const struct bt_gatt_attr *attr, uint16_t value)
{
    /* TODO: Handle CCC value */
}

// Audio read setup, again not needed for assignment but required for service
static ssize_t read_audio(struct bt_conn *conn, const struct bt_gatt_attr *attr,
                           void *buf, uint16_t len, uint16_t offset)
{
    if (offset > sizeof(audio_pcm_value)) {
        return BT_GATT_ERR(BT_ATT_ERR_INVALID_OFFSET);
    }

    return bt_gatt_attr_read(conn, attr, buf, len, offset,
                              &audio_pcm_value + offset, sizeof(audio_pcm_value) - offset);
}

// Audio write functionality for audio buffer
static ssize_t write_audio(struct bt_conn *conn, const struct bt_gatt_attr *attr,
                            const void *buf, uint16_t len, uint16_t offset,
                            uint8_t flags)
{
    if (offset + len > sizeof(audio_pcm_value)) {
        return BT_GATT_ERR(BT_ATT_ERR_INVALID_OFFSET);
    }

    memcpy(&audio_pcm_value + offset, buf, len);
    audio_update = 1;

    return len;
}

// Service definition for the audio advertisement
BT_GATT_SERVICE_DEFINE(audio_svc,
    BT_GATT_PRIMARY_SERVICE(BT_UUID_CTS),
    BT_GATT_CHARACTERISTIC(BT_UUID_CTS_CURRENT_TIME, BT_GATT_CHRC_READ |
			       BT_GATT_CHRC_NOTIFY | BT_GATT_CHRC_WRITE,
			       BT_GATT_PERM_READ | BT_GATT_PERM_WRITE,
			       read_audio, write_audio, NULL),
    BT_GATT_CCC(audio_ccc_cfg_changed, BT_GATT_PERM_READ | BT_GATT_PERM_WRITE),
);



void audio_notify(uint16_t* buffer)
{
    uint16_t sample;

    for (int i = 0; i < BUF_SIZE; i++) {

        sample = buffer[i];
        bt_gatt_notify(NULL, &audio_svc.attrs[1], &sample, sizeof(sample));
        
    }
    
    
}
