#include <iostream>

int add(int a, int b) {
    return a + b;
}

int main() {
    int x = 5;
    int y = 10;
    int z = add(x, y);
    std::cout << "The sum of " << x << " and " << y << " is " << z << std::endl;
    return 0;
}