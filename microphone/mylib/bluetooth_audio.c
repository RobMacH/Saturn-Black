/* main.c - Application main entry point */

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

bool hrf_ntf_enabled;
// Queue to be accessed outside of the module
extern struct k_msgq recv_msgq;

// int connected_stat = 0;

// Construct data structure for PCM values
static const struct bt_data ad[] = {
    BT_DATA_BYTES(BT_DATA_FLAGS, (BT_LE_AD_GENERAL | BT_LE_AD_NO_BREDR)),
    BT_DATA_BYTES(BT_DATA_UUID16_ALL, BT_UUID_16_ENCODE(BT_UUID_AUDIO_VAL))
};

// Connected flag
static void connected(struct bt_conn *conn, uint8_t err)
{
    if (err) {
        printk("Connection failed (err 0x%02x)\n", err);
    } else {
        printk("Connected\n");
        // connected = 1;
    }
}

// Disconnection flag
static void disconnected(struct bt_conn *conn, uint8_t reason)
{
    printk("Disconnected (reason 0x%02x)\n", reason);
}

// Callback definition
BT_CONN_CB_DEFINE(conn_callbacks) = {
    .connected = connected,
    .disconnected = disconnected,
};

// Toggle the enable variable
static void hrs_ntf_changed(bool enabled)
{
	hrf_ntf_enabled = enabled;

	printk("HRS notification status changed: %s\n", enabled ? "enabled" : "disabled");
}

// Callback struct for values changed
static struct bt_hrs_cb hrs_cb = {
	.ntf_changed = hrs_ntf_changed,
};

// Initalise bluetooth on thingy
static void bt_ready(void)
{
    int err;

    printk("Bluetooth initialized\n");

    // Start bluetooth advertising
    err = bt_le_adv_start(BT_LE_ADV_CONN_NAME, ad, ARRAY_SIZE(ad), NULL, 0);
    if (err) {
        printk("Advertising failed to start (err %d)\n", err);
        return;
    }

    printk("Advertising successfully started\n");
}

// Cancel connection
static void auth_cancel(struct bt_conn *conn)
{
    char addr[BT_ADDR_LE_STR_LEN];

    bt_addr_le_to_str(bt_conn_get_dst(conn), addr, sizeof(addr));

    printk("Pairing cancelled: %s\n", addr);
}

// Cancel cb function struct
static struct bt_conn_auth_cb auth_cb_display = {
    .cancel = auth_cancel,
};

// Bluetooth audio thread for initalising and reading PCM data
int bluetooth_audio_init(void)
{
    int err;
    uint8_t recv_data[3200];

    err = bt_enable(NULL);
    if (err) {
        printk("Bluetooth init failed (err %d)\n", err);
        return 0;
    }

    bt_ready();

    // Register call back functions
    bt_conn_auth_cb_register(&auth_cb_display);
    bt_hrs_cb_register(&hrs_cb);
    /* Implement notification. At the moment there is no suitable way
    * of starting delayed work so we do it here
    */
  
    while (1) {

        if (k_msgq_get(&recv_msgq, &recv_data, K_FOREVER) == 0) {

            audio_notify(recv_data);
            
            memset(recv_data, 0, sizeof(recv_data));

        }

    }
    return 0;
}
