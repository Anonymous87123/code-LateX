#include <iostream>
using namespace std;

class Animal {
public:
    ~Animal() {
        cout << "Animal 析构" << endl;
    }
};

class Dog : public Animal {
private:
    int* data;

public:
    Dog() {
        data = new int[100];
        cout << "Dog 构造，申请资源" << endl;
    }

    ~Dog() {
        delete[] data;
        cout << "Dog 析构，释放资源" << endl;
    }
};

int main() {
    Animal* p = new Dog;

    delete p;

    return 0;
}