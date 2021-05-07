import os
import platform





def shutdown(time):
    OS_type = platform.system()
    OS_type = OS_type.lower()
    shutdown_str=""
    if OS_type == 'linux':
        time = time /60
        shutdown_str = 'shutdown -t '+ str(time)
    elif OS_type == 'windows':
        #time = time * 60
        shutdown_str = 'shutdown -s -t ' + str(time)
    else:
        print('Sorry this feature is not available in ', OS_type)
        return

    os.system(shutdown_str)

def cancel_shutdown():
    OS_type = platform.system()
    OS_type = OS_type.lower()
    if OS_type == 'linux':
        cancel_str = 'shutdown -c'
    elif OS_type == 'windows':
        cancel_str = 'shutdown -a'
    else:
        return
    os.system(cancel_str)

# # def main():
# #     print('Use Shutup To schedule your shutdown'.center(50, '='))
# #     print('1.Automate Shutdown\n2.Cancel shutdown')
# #     option = int(input('Option here: '))
# #     if option == 1:
# #         time = int(input('\nEnter time to shutdown in Minutes : '))
# #         shutdown(time)
# #     elif option == 2:
# #         cancel_shutdown()
# #         print('Shutdown successful canceled ...')
# #     else:
# #         print('Invalid option try again!!!\n')
# #         main()

# # main()