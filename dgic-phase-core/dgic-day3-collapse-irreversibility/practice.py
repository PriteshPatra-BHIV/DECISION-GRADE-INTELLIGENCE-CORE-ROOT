# def func(x,n):
#     if n==0:
#         return
#     else:
#         print(x)
#         func(x,n-1)

# func("Pritesh",7)

# def pfucn(i,n):
#     if i>n:
#         return
#     else:
#         pfucn(i+1,n)
#         print(i)
# pfucn(0,5)

# def ppfunc(n):
#     if n==0:
#         return
#     else:
#         ppfunc(n-1)
#         print(n)
# ppfunc(5)


# paramerized recursion
# def sum12(n,i,sum):
#     if i>n:
#         print(sum)
#         return
#     else:
#         sum12(n,i+1,sum+i)

# print(sum12(5,0,0))

#functional recursion
# def sum11(n):
#     if n==0:
#         return 0
#     else:
#         return (n + sum11(n-1))
# print(sum11(4))

# n = 0

# while n<11:
#     print("*",end="")
#     n = n + 1
# print()

# n = 0
# while n<6:
#     print("*",end="")
#     n = n + 1
# print()

# n=0
# while n<5:
#     print("*",end=""
#     n = n + 1

# def fact(n):
#     if n==0 or n==1:
#         return 1 
#     else:
#         return n*fact(n-1)
# print(fact(4))

# str = "Pritesh"
# rstr = str[::-1]
# print(rstr)

# def rstr(arr,left,right):
#     if left>=right:
#         return arr
#     else:
#         arr[left],arr[right] = arr[right],arr[left]
#         return rstr(arr,left+1,right-1)
# print(rstr(["P","r","i","t","e","s","h"],1,5))

# str = "Pritesh"
# rstr = str[::-1]
# print(rstr)

# if str == rstr:
#     print("Palindrome")
# else:
#     print("Not Palindrome")

import datetime

day = datetime.date(2010,1,10)
print(day.strftime("%A"))