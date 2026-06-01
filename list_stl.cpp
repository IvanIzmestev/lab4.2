#include <iostream>
#include <list>
#include <algorithm>

std::list<int> myList;

extern "C" {

__declspec(dllexport) void add_first(int value) {
    myList.push_front(value);
}

__declspec(dllexport) void remove_first() {
    if (!myList.empty()) {
        myList.pop_front();
    }
}

__declspec(dllexport) int get_count() {
    return myList.size();
}

__declspec(dllexport) int get_value(int index, int* out) {
    if (index < 0 || index >= (int)myList.size()) {
        return 0; // Индекс вне диапазона
    }
    
    auto it = myList.begin();
    std::advance(it, index);
    *out = *it;
    return 1;
}

__declspec(dllexport) void clear_list() {
    myList.clear();
}

__declspec(dllexport) void add_last(int value) {
    myList.push_back(value);
}

__declspec(dllexport) void remove_last() {
    if (!myList.empty()) {
        myList.pop_back();
    }
}

__declspec(dllexport) int add_by_index(int index, int value) {
    if (index < 0 || index > (int)myList.size()) {
        return 0; // Неверный индекс
    }
    
    auto it = myList.begin();
    std::advance(it, index);
    myList.insert(it, value);
    return 1;
}

__declspec(dllexport) int remove_by_index(int index) {
    if (index < 0 || index >= (int)myList.size()) {
        return 0; // Неверный индекс
    }
    
    auto it = myList.begin();
    std::advance(it, index);
    myList.erase(it);
    return 1;
}

__declspec(dllexport) int remove_by_condition(int value, int mode) {
    // mode: 1 - меньше, 2 - равно, 3 - больше
    int removed_count = 0;
    
    auto it = myList.begin();
    while (it != myList.end()) {
        bool should_remove = false;
        
        switch(mode) {
            case 1: should_remove = (*it < value); break;
            case 2: should_remove = (*it == value); break;
            case 3: should_remove = (*it > value); break;
            case 4: should_remove = (*it <= value); break;
            default: return 0;
        }
        
        if (should_remove) {
            it = myList.erase(it);
            removed_count++;
        } else {
            ++it;
        }
    }
    
    return removed_count;
}


__declspec(dllexport) int find_first(int value) {
    auto it = std::find(myList.begin(), myList.end(), value);
    if (it != myList.end()) {
        return std::distance(myList.begin(), it);
    }
    return -1;
}

__declspec(dllexport) void reverse_list() {
    myList.reverse();
}

__declspec(dllexport) void sort_list() {
    myList.sort();
}

__declspec(dllexport) int get_min(int* out) {
    if (myList.empty()) return 0;
    *out = *std::min_element(myList.begin(), myList.end());
    return 1;
}

__declspec(dllexport) int get_max(int* out) {
    if (myList.empty()) return 0;
    *out = *std::max_element(myList.begin(), myList.end());
    return 1;
}

__declspec(dllexport) void remove_duplicates() {
    myList.sort();
    myList.unique();
}

}