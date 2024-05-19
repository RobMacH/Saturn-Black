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
#include <zephyr/sys/util.h>
#include <zephyr/bluetooth/byteorder.h>



// Audio value and update flag 
// static uint64_t audio_pcm_value = 0;
static uint8_t audio_update = 0;

static uint64_t audio_buff[400];

// Function for CCC value, required but not necessary for our functionality
static void audio_ccc_cfg_changed(const struct bt_gatt_attr *attr, uint16_t value)
{
    /* TODO: Handle CCC value */
}

// Audio read setup, again not needed for assignment but required for service
static ssize_t read_audio(struct bt_conn *conn, const struct bt_gatt_attr *attr,
                           void *buf, uint16_t len, uint16_t offset)
{
    if (offset > sizeof(audio_buff)) {
        return BT_GATT_ERR(BT_ATT_ERR_INVALID_OFFSET);
    }

    return bt_gatt_attr_read(conn, attr, buf, len, offset,
                              &audio_buff + offset, sizeof(audio_buff) - offset);
}

// Audio write functionality for audio buffer
static ssize_t write_audio(struct bt_conn *conn, const struct bt_gatt_attr *attr,
                            const void *buf, uint16_t len, uint16_t offset,
                            uint8_t flags)
{
    if (offset + len > sizeof(audio_buff)) {
        return BT_GATT_ERR(BT_ATT_ERR_INVALID_OFFSET);
    }

    memcpy(&audio_buff + offset, buf, len);
    audio_update = 1;

    return len;
}

// Service definition for the audio advertisement
BT_GATT_SERVICE_DEFINE(audio_svc,
    BT_GATT_PRIMARY_SERVICE(BT_UUID_CTS),
    BT_GATT_CHARACTERISTIC(BT_UUID_CTS_CURRENT_TIME, BT_GATT_CHRC_READ |
			       BT_GATT_CHRC_NOTIFY | BT_GATT_CHRC_WRITE,
			       BT_GATT_PERM_READ | BT_GATT_PERM_WRITE,
			       NULL, NULL, NULL),
    BT_GATT_CCC(audio_ccc_cfg_changed, BT_GATT_PERM_READ | BT_GATT_PERM_WRITE),
);

// Function to broadcast the pcm value through the service
void audio_notify(uint64_t* pcm_value)
{
    // if (!audio_update) {
    //     printk("Nothing\n");
    //     return;

    for (int i = 0; i < 400; i+=2) {

        bt_gatt_notify(NULL, &audio_svc.attrs[1], &(pcm_value[i]), 16);

    }
}