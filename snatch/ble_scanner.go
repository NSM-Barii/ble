package ble

import (
	"fmt"
	"time"

	"tinygo.org/x/bluetooth"
)


var adapter = bluetooth.DefaultAdapter

type BLE struct {
	Name string
	Addr string
	RSSI int16
	UUID         []bluetooth.UUID
	Manufacturer []bluetooth.ManufacturerDataElement
}


func BLE_Scanner() {
	// This method will be responsible for performing BLE Scan

	if err := adapter.Enable();  err != nil{
		fmt.Println(err)
	}


	// LIST
	devices := []BLE{}
    

	fmt.Println("[+] Launching BLE Scanner...")


	err := adapter.Scan(func(a *bluetooth.Adapter, b bluetooth.ScanResult) {



		name := b.LocalName()
		addr := b.Address.String()
		rssi := b.RSSI          
		uuid := b.ServiceUUIDs()
		manuf := b.ManufacturerData()

        
		fmt.Println("-----------")
	    fmt.Println("Name: ", name)
		fmt.Println("Addr: ", addr)
		fmt.Println("RSSi: ", rssi)
		fmt.Println("uuid: ", uuid)
		fmt.Println("Manufacturer: ", manuf)




		device := BLE{
			Name: name,
			Addr: addr,
			RSSI: rssi,
			UUID: uuid,
			Manufacturer: manuf,

		}


		devices = append(devices, device)


	})


	if err != nil{
		fmt.Println(err)
	}



}






func Main(){

	go BLE_Scanner()

	fmt.Println("[*] Thread 1 Started")


	<-time.After(5 * time.Second)
	adapter.StopScan()
	println("[-] Terminated BLE Scan!")
	//println("Total Devices Found: ", len(BLE_Scanner.devices))
}
