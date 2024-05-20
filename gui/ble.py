import simplepyble
import time
import pyaudio
import wave
import array
# from threading import Semaphore
import settings

arr = bytearray()
count = 0


def test():
    
    with open("untitled.raw", "rb") as in_f:
        data = in_f.read()
    
    for i in range(len(data) - 2):
        byte16 = bytes(data[i:i+2])
        print(int.from_bytes(byte16, 'little'))
   

    # print(int.from_bytes(data[200:202], 'big'))
    #

    # print(type(data[0:2]))

    """ The below code works, define the stream then just write a bytes array to the stream and it plays back the audio 
        Input to write() is the frames (data) and the length of frames (len(frames) / 2) since each value in data is 1 byte but our audio samples are 2 bytes"""
    # p = pyaudio.PyAudio()

    # stream = p.open(format=pyaudio.paInt16,
    #                 channels=1,
    #                 rate=16000,
    #                 output=True)

    # stream.write(data, int(214464/2))

def audio_callback(data):

    global arr
    global count
    print(data)
    count+=1
    print(count)
    # if settings.recording == 1:
    # if len(arr) >= 100000:
    #     print("Finished Recording")
    #     # a = bytes(arr)
    #     with wave.open("sound.wav", "wb") as out_f:
    #             out_f.setnchannels(1)
    #             out_f.setsampwidth(2)
    #             out_f.setframerate(16000)
    #             out_f.writeframes(arr)
    #     arr = bytearray()
    # else:
    #     arr.extend(data)
    #     # print(data)
    #     print(len(arr))


def record():

    adapters = simplepyble.Adapter.get_adapters()

    if len(adapters) == 0:
        print("No adapters found")

    # Query the user to pick an adapter
    print("Please select an adapter:")
    for i, adapter in enumerate(adapters):
        print(f"{i}: {adapter.identifier()} [{adapter.address()}]")

    choice = int(input("Enter choice: "))
    adapter = adapters[choice]

    print(f"Selected adapter: {adapter.identifier()} [{adapter.address()}]")

    adapter.set_callback_on_scan_start(lambda: print("Scan started."))
    adapter.set_callback_on_scan_stop(lambda: print("Scan complete."))
    adapter.set_callback_on_scan_found(lambda peripheral: print(f"Found {peripheral.identifier()} [{peripheral.address()}]"))

    # Scan for 5 seconds
    adapter.scan_for(5000)
    peripherals = adapter.scan_get_results()

    # Query the user to pick a peripheral
    print("Please select a peripheral:")
    for i, peripheral in enumerate(peripherals):
        print(f"{i}: {peripheral.identifier()} [{peripheral.address()}]")

    choice = int(input("Enter choice: "))
    peripheral = peripherals[choice]

    print(f"Connecting to: {peripheral.identifier()} [{peripheral.address()}]")
    peripheral.connect()

    print("Successfully connected, listing services...")
    services = peripheral.services()
    service_characteristic_pair = []
    for service in services:
        for characteristic in service.characteristics():
            service_characteristic_pair.append((service.uuid(), characteristic.uuid()))

    # Query the user to pick a service/characteristic pair
    print("Please select a service/characteristic pair:")
    for i, (service_uuid, characteristic) in enumerate(service_characteristic_pair):
        print(f"{i}: {service_uuid} {characteristic}")

    choice = int(input("Enter choice: "))
    service_uuid, characteristic_uuid = service_characteristic_pair[choice]

    try:
        content = peripheral.notify(service_uuid, characteristic_uuid, audio_callback)
        while True:
            pass
    except KeyboardInterrupt:
        peripheral.disconnect()
        

#     with wave.open("sound.wav", "wb") as out_f:
#         out_f.setnchannels(1)
#         out_f.setsampwidth(2)
#         out_f.setframerate(44100)
#         out_f.writeframes(a)
    
#     peripheral.disconnect()
    
#     # with wave.open("sound.wav", "rb") as in_f:
#     #     print(repr(in_f.getparams()))


    
# # def hex_to_binary(input_file_path, output_file_path):
# #     with open(input_file_path, 'r') as file:
# #         lines = file.readlines()

# #     with open(output_file_path, 'wb') as binary_file:
# #         for line in lines:
# #             hex_values = line.strip().split()
# #             for value in hex_values:
# #                 binary_value = int(value, 16).to_bytes(2, byteorder='little')
# #                 binary_file.write(binary_value)



    



def main():

    record()



if __name__ == '__main__':
    main()
    # test()
