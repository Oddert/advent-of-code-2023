# for i in range(3):

#     print(f"Outer loop iteration: {i}")
    
#     for j in range(3):
#         print(f"    Inner loop iteration: {j}")
        
#         while True:
#             print("        Inside while loop")
            
#             if j == 1:
#                 continue
            
#             print("        Still inside while loop after continue")
#             break  # This will break out of the while loop

x = 0
while x < 10:
    print('While', x)
    for i in range(3):
        print('For 1', i)
        for j in range(3):
            print('For 2', j)
            if i == 2 and j == 2:
                print('> breaking')
                break
            print('Reachable')
            continue
            print('Not Reachable')
    x += 1
