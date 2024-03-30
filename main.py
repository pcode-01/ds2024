# from list.listNode import ListNode
# from list.linkedListBasic import LinkedListBasic
from list.circularLinkedList import CircularLinkedList

if __name__ == "__main__":
    names = ["Amy", "Kevin", "Mary", "David"]

    # name_list = LinkedListBasic()
    name_list = CircularLinkedList()

    for name in names:
        name_list.append(name)

    for name in name_list:
        print(name)

    name_list.pop(-1) 
    name_list.insert(0, "Rose")
    name_list.sort()
    name_list.printList()
