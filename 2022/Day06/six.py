with open('input.txt', 'r') as f:
    charstream = f.readline()

has_packet = False
has_message = False

for i in range(3, len(charstream)):
    packet = set(charstream[i-3:i+1])
    if len(packet) == 4 and not has_packet:
        # add one b/c problem is one-indexed
        print('Packet starts at', i + 1)
        has_packet = True
    
    try:
        message = set(charstream[i-13:i+1])
        if len(message) == 14 and not has_message:
            print('Message starts at', i+1)
            has_message = True
    except IndexError:
        pass

    if has_message and has_packet:
        break
        

