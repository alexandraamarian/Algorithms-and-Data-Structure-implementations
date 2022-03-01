from avl_node import AVLNode

class AVLTree:

    def __init__(self):
        """Default constructor. Initializes the AVL tree.
        """
        self.root = None
        self.size = 0
        self.currentNode = AVLNode()
        self.list = []
        self.list_key_inorder =[]
        self.list_value_inorder=[]

    def get_tree_root(self):

        return self.root

    def get_tree_height(self):

        if not self.root:
            return -1
        else:
            return self.root.height

    def get_tree_size(self):
        """Yields number of key/value pairs in the tree.
        :return Number of key/value pairs.
        """
        if self.root is not None:
            return len(self.list_key_inorder)
        else:
            return 0

    def to_array(self):
        """Yields an array representation of the tree's values (pre-order).
        :return Array representation of the tree values.
        """

        self.preorder(self.root)
        return self.list

    def preorder(self, root: AVLNode):
        if root:
            self.list.append(root.value)
            self.preorder(root.left)
            self.preorder(root.right)
    def print_tree(self, root):
        if root:
            print(f"value: {root.value} key: {root.key} height: {root.height}")
            self.print_tree(root.left)
            self.print_tree(root.right)

    def AddPair (self, node: AVLNode):
        if node is not None :
            self.list_key_inorder.append(node.key)
            self.list_value_inorder.append(node.value)

    def find_by_key(self, key):
        """Returns value of node with given key.
        :param key: Key to search.
        :return Corresponding value if key was found, None otherwise.
        :raises ValueError if the key is None
        """
        for i in range (len(self.list_key_inorder)):
            if self.list_key_inorder[i] is key :
                return self.list_value_inorder[i]
        return None
        #rise value error
    def _find_by_key(self, key, currentnode):
        if currentnode is not None:
            if currentnode.key == key:
                return currentnode
            else:
                if currentnode.left is not None:
                    currentnode_left = self._find_by_key(key, currentnode.left)
                    if currentnode_left is not None:
                        return currentnode_left
                if currentnode.right is not None:
                    currentnode_right = self._find_by_key(key, currentnode.right)
                    if currentnode_right is not None:
                        return currentnode_right

    def insert(self, key, value):

        new_node = AVLNode(key,value)

        if self.root is None:
            self.root = new_node
            self.size = self.size + 1
            self.AddPair(new_node)
            return True

        if self.find_by_key(key) is not None:
            return False

        if key is None or value is None:
            raise ValueError

        else:
            self.insertNew_Node(key, value, self.root)
            self.AddPair ( new_node )

    def insertNew_Node(self, key, value, current_node: AVLNode):

        new_node = AVLNode(key,value)
        if value < current_node.value:

            if current_node.left is None:

                current_node.left = new_node
                current_node.left.parent = current_node
                self.verify_insertion(current_node.left)
                self.size = self.size + 1
                return True

            else:

                self.insertNew_Node(key, value, current_node.left)

        elif value > current_node.value:

            if current_node.right is None:

                current_node.right = new_node
                current_node.right.parent = current_node
                self.verify_insertion(current_node.right)
                self.size= self.size + 1
                return True

            else:
                self.insertNew_Node(key, value, current_node.right)

    def get_height_of_node(self, node: AVLNode):
        if node is not None:
            return node.height
        return -1

    def verify_insertion(self, currentnode: AVLNode, l=[]):

        parent_of_currentnode = currentnode.parent
        if parent_of_currentnode is None:
            return

        Height_of_left_part = self.get_height_of_node(parent_of_currentnode.left)
        Height_of_right_part = self.get_height_of_node(parent_of_currentnode.right)

        l = [currentnode] + l

        if abs(Height_of_left_part - Height_of_right_part) > 1:

            l = [parent_of_currentnode] + l
            self.Balancing(l[0], l[1], l[2])
            return

        the_new_height = 1 + currentnode.height

        if the_new_height > parent_of_currentnode.height:
            parent_of_currentnode.height = the_new_height

        self.verify_insertion(currentnode.parent, l)

    def rightRotate(self, node: AVLNode):
        parent = node.parent
        child = node.left
        aux = child.right
        child.right = node
        node.parent = child
        node.left = aux

        if aux is not None:
            aux.parent = node

        child.parent = parent

        if child.parent is None:
            self.root = child
        else:
            if child.parent.left == node:
                child.parent.left = child
            else:
                child.parent.right = child

        node.height = 1 + max( self.get_height_of_node(node.right),self.get_height_of_node(node.left),)
        child.height = 1 + max( self.get_height_of_node(child.right),self.get_height_of_node(child.left))

    def leftRotate(self, node: AVLNode):
        parent = node.parent
        child = node.right
        aux = child.left
        child.left = node
        node.parent = child
        node.right = aux
        if aux is not None:

            aux.parent = node

        child.parent = parent

        if child.parent is None:
            self.root = child
        else:
            if child.parent.left == node:
                child.parent.left = child
            else:
                child.parent.right = child

        node.height = 1 + max( self.get_height_of_node(node.right),self.get_height_of_node(node.left))
        child.height = 1 + max( self.get_height_of_node(child.right),self.get_height_of_node(child.left))

    def Balancing(self, grandparent, parent, current_node: AVLNode):

        if parent == grandparent.left and current_node == parent.left:
            self.rightRotate(grandparent)

        elif parent == grandparent.right and current_node == parent.right:
            self.leftRotate(grandparent)

        elif parent == grandparent.right and current_node == parent.left:
            self.rightRotate(parent)
            self.leftRotate(grandparent)

        elif parent == grandparent.left and current_node == parent.right:
            self.leftRotate(parent)
            self.rightRotate(grandparent)

    def leftmost_node(self, currentnode: AVLNode):
        while currentnode.left is not None:
            currentnode = currentnode.left
        return currentnode

    def rightmost_node(self, currentnode: AVLNode):
        while currentnode.right is not None:
            currentnode = currentnode.right
        return currentnode

    def find_number_of_children(self, currentnode: AVLNode):
        children = 0

        if currentnode.left is not None :
            children = children + 1
        if currentnode.right is not None :
            children = children + 1
        return children

    def remove_by_key(self, key):
        """Removes node with given key.
        :param key: Key of node to remove.
        :return True If node was found and deleted, False otherwise.
        @raises ValueError if the key is None.
        """
        x = self._find_by_key(key,self.root)
        if x is None:
            return False

        else:
            node_to_be_deleted = x
            self.delete_one_node(node_to_be_deleted)
        return True

    def delete_one_node(self, currentnode: AVLNode):

        if currentnode is None:
            return False

        parent = currentnode.parent
        node_number_of_children = self.find_number_of_children(currentnode)


        if node_number_of_children == 0:

            if parent is None:
                self.list_key_inorder.remove(self.root.key)
                self.list_value_inorder.remove(self.root.value)
                self.root = None
                self.size = self.size - 1

            elif parent is not None:

                if parent.right is currentnode:
                    temp = currentnode
                    self.list_key_inorder.remove(temp.key)
                    self.list_value_inorder.remove(temp.value)
                    parent.right = None

                    self.size = self.size - 1

                elif parent.left is currentnode:
                    temp = currentnode
                    self.list_key_inorder.remove(temp.key)
                    self.list_value_inorder.remove(temp.value)
                    parent.left = None
                    self.size = self.size - 1


        if node_number_of_children == 1:
            child = None
            if currentnode.left is not None:
                child = currentnode.left
            elif currentnode.right is not None:
                child = currentnode.right
            if parent is None and child:
                temp = child
                self.list_key_inorder.remove(temp.key)
                self.list_value_inorder.remove(temp.value)
                self.root = child
                child = None
                self.size = self.size - 1
            else:
                if parent.left is currentnode:
                    temp = child
                    self.list_key_inorder.remove(temp.key)
                    self.list_value_inorder.remove(temp.value)
                    parent.left = child
                    self.size = self.size - 1
                    child = None


                elif parent.right is currentnode:
                    temp = child
                    self.list_key_inorder.remove(temp.key)
                    self.list_value_inorder.remove(temp.value)
                    parent.right = child
                    self.size = self.size - 1
                    child = None
            child.parent = parent

        if node_number_of_children == 2:


            temp = currentnode
            self.list_key_inorder.remove(temp.key)
            self.list_value_inorder.remove(temp.value)
            successor = self.leftmost_node(currentnode.right)
            currentnode.value = successor.value
            currentnode.key = successor.key
            self.delete_one_node(successor)
            self.list_key_inorder.append(successor.key)
            self.list_value_inorder.append(successor.value)
            self.size = self.size - 1
            return
        if parent is not None:
            parent.height = 1 + max(self.get_height_of_node(parent.left), self.get_height_of_node(parent.right))
            self.verify_deletion(parent)


    def verify_deletion(self, currentnode: AVLNode):

        if currentnode.parent is None:
            currentnode.height = 1+ max(self.get_height_of_node(currentnode.left), self.get_height_of_node(currentnode.right))
            return

        height_of_left_part = self.get_height_of_node(currentnode.left)
        height_of_right_part = self.get_height_of_node(currentnode.right)

        if abs(height_of_left_part - height_of_right_part)>1:
            node_1 = self.find_taller_child(currentnode)
            node_2 = self.find_taller_child(node_1)
            self.Balancing(currentnode,node_1,node_2)

        self.verify_deletion(currentnode.parent)

    def find_taller_child(self, node:AVLNode):

        leftpart = self.get_height_of_node(node.left)
        rightpart = self.get_height_of_node(node.right)

        if leftpart > rightpart:
            return node.left
        else:
            return node.right
