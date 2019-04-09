#include<iostream>

using namespace std;

struct Node {
   int data;
   struct Node *next;
};
class List {
private:
   Node *head;
public:
   List() {head = NULL;}
   bool isEmpty();
   void InsertNode(int num);
   void DeleteNode(int num);
   void traverse();
   int searchNode(int num);
   void Reverse();
   ~List();
};
int main() {
    List ll;
    ll.DeleteNode(10);
    ll.InsertNode(10);
    ll.InsertNode(5);
    ll.traverse();
    ll.InsertNode(30);
    ll.searchNode(5);
    ll.DeleteNode(5);
    ll.traverse();
}

bool List::isEmpty() {
   if (head == NULL) return true;
   else return false;
}
void List::InsertNode(int num) {
   Node *temp = new Node();
   temp->data = num;
   Node *p, *q;

   if (head == NULL) {
      temp->data = num;
      head = temp;
   }
   else if (temp->data < head->data) {
      temp->next = head;
      head = temp;
   }
   else {
      p = head;
      while (p != NULL && temp->data > p->data) {
         q = p;
         p = p->next;
      }
      if (p != NULL) {
         temp->next = p;
         q->next = temp;
      }
      else {
         q->next = temp;
      }
   }

}
void List::DeleteNode(int num) {
   Node *p, *q;

   if (head->data == num) {
      p = head;
      head = head->next;
      delete p;
   }
   else {
      p = head;
      while (p != NULL && p->data != num) {
         q = p;
         p = p->next;
      }
      if (p != NULL) {
         q->next = p->next;
         delete p;
      }
      else
         cout << num << "is not in the list\n";
   }
}
void List::traverse() {
   Node *p;

   if (!isEmpty()) {
      p = head;
      while (p) {
         cout << p->data << " ";
         p = p->next;
      }
      cout << endl;
   }
   else {
      cout << "List is empty!\n";
   }
}
int List::searchNode(int num) {
   Node *p, *q;
   p = head;
   while (p != NULL && p->data != num) {
      q = p;
      p = p->next;
   }
   if (p != 0) return 1;
   else return 0;
}
List::~List(){
   Node *p;
   while (head != 0) {
      p = head;
      head = head->next;
      delete p;
   }
}
void List::Reverse() {
   Node *p, *q, *r;
   p = head;
   q = NULL;

   while (p) {
      r = q;
      q = p;
      p = p->next;
      q->next = r;
   }
   head = q;
}
