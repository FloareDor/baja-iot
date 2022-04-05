/**
 * Example program for basic use of pico as an I2C peripheral (previously known as I2C slave)
 * 
 * This example allows the pico to act as a 256byte RAM
 * 
 * Author: Graham Smith (graham@smithg.co.uk)
 */


// Usage:
//
// When writing data to the pico the first data byte updates the current address to be used when writing or reading from the RAM
// Subsequent data bytes contain data that is written to the ram at the current address and following locations (current address auto increments)
//
// When reading data from the pico the first data byte returned will be from the ram storage located at current address
// Subsequent bytes will be returned from the following ram locations (again current address auto increments)
//
// N.B. if the current address reaches 255, it will autoincrement to 0 after next read / write


#include "pico/stdlib.h"
#include "hardware/i2c.h"
#include "hardware/irq.h"

// define I2C addresses to be used for this peripheral
#define I2C1_PERIPHERAL_ADDR 0x31

// GPIO pins to use for I2C
#define GPIO_SDA1 14
#define GPIO_SCK1 15
#define LED_PIN 25


// ram_addr is the current address to be used when writing / reading the RAM
// N.B. the address auto increments, as stored in 8 bit value it automatically rolls round when reaches 255
uint8_t ram_addr = 0;

// ram is the storage for the RAM data
uint8_t ram[256];


// Interrupt handler implements the RAM
void i2c1_irq_handler() {

	// Get interrupt status
	uint32_t status = i2c1->hw->intr_stat;

	// Check to see if we have received data from the I2C controller
	if (status & I2C_IC_INTR_STAT_R_RX_FULL_BITS) {

		// Read the data (this will clear the interrupt)
		uint32_t value = i2c1->hw->data_cmd;

		// Check if this is the 1st byte we have received
		if (value & I2C_IC_DATA_CMD_FIRST_DATA_BYTE_BITS) {

			// If so treat it as the address to use
			ram_addr = (uint8_t)(value & I2C_IC_DATA_CMD_DAT_BITS);

		} else {
			// If not 1st byte then store the data in the RAM
			// and increment the address to point to next byte
			ram[ram_addr] = (uint8_t)(value & I2C_IC_DATA_CMD_DAT_BITS);
			ram_addr++;
		}
	}

	// Check to see if the I2C controller is requesting data from the RAM
	if (status & I2C_IC_INTR_STAT_R_RD_REQ_BITS) {

		// Write the data from the current address in RAM
		i2c1->hw->data_cmd = (uint32_t)ram[ram_addr];

		// Clear the interrupt
		i2c1->hw->clr_rd_req;

		// Increment the address
		ram_addr++;
	}
}


// Main loop - initilises system and then loops while interrupts get on with processing the data
int main()
{

	// Testing sending data
	for(int i = 0; i < 256; i++)
		ram[i] = 255 - i;

	// Set the led up to know Pi is alive
	gpio_init(LED_PIN);
	gpio_set_dir(LED_PIN, GPIO_OUT);
	gpio_put(LED_PIN, 1);

	// Setup I2C1 as slave (peripheral)
	i2c_init(i2c1, 100 * 1000);
	i2c_set_slave_mode(i2c1, true, I2C1_PERIPHERAL_ADDR);

	// Setup GPIO pins to use and add pull up resistors
	gpio_set_function(GPIO_SDA1, GPIO_FUNC_I2C);
	gpio_set_function(GPIO_SCK1, GPIO_FUNC_I2C);
	gpio_pull_up(GPIO_SDA1);
	gpio_pull_up(GPIO_SCK1);

	// Enable the I2C interrupts we want to process
	i2c1->hw->intr_mask = (I2C_IC_INTR_MASK_M_RD_REQ_BITS | I2C_IC_INTR_MASK_M_RX_FULL_BITS);

	// Set up the interrupt handler to service I2C interrupts
	irq_set_exclusive_handler(I2C1_IRQ, i2c1_irq_handler);

	// Enable I2C interrupt
	irq_set_enabled(I2C1_IRQ, true);

	// Do nothing in main loop
	while (true) {
		tight_loop_contents();
	}
	return 0;
}