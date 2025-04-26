#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define MAX_WORD_LENGTH 5
#define MAX_WORDS 500

bool visited[MAX_WORDS];
int path_cnt = 0;
int max_length = 500;


int findYulMyungPaths(const char *yul, const char *myung, char **wordList, int wordListSize);
bool isOneLetterDiff(const char *a, const char *b);
void reverseString(const char *src, char *dst);
bool isEmpty();

void clear_input_buffer();

int main() {
    char yul[MAX_WORD_LENGTH+1], myung[MAX_WORD_LENGTH+1];
	  char line[(MAX_WORDS+1)*(MAX_WORD_LENGTH + 1)+1];
    char *wordList[MAX_WORDS];
    int wordListSize = 0;

    printf("Enter yul: ");
    scanf("%s", yul);
    clear_input_buffer();  // Clear the newline left by scanf

    printf("Enter myung: ");
    scanf("%s", myung);
    clear_input_buffer();  // Clear the newline left by scanf


    printf("Enter words separated by spaces: ");
    if (fgets(line, sizeof(line), stdin)) {
        // Remove trailing newline, if any
        line[strcspn(line, "\n")] = 0;

        // Tokenize the input string
        char *token = strtok(line, " ");
        while (token != NULL && wordListSize < MAX_WORDS) {
            wordList[wordListSize] = malloc(strlen(token) + 1);
            if (wordList[wordListSize] == NULL) {
                fprintf(stderr, "Memory allocation failed\n");
                return 1;
            }
            strcpy(wordList[wordListSize], token);
            wordListSize++;
            token = strtok(NULL, " ");
        }
    }

    
    int result = findYulMyungPaths(yul, myung, wordList, wordListSize);
    printf("Total paths with minimum word transformation: %d\n", result);

    // Free allocated memory
    for (int i = 0; i < wordListSize; i++) {
        free(wordList[i]);
    }

    return 0;
}
void clear_input_buffer() {
    int c;
    while ((c = getchar()) != '\n' && c != EOF) { }
}

bool isOneLetterDiff(const char *a, const char *b) {
    int len = strlen(a);
    if (strlen(b) != len) return false;
    int diff = 0;
    for (int i = 0; i < len; i++) {
        if (a[i] != b[i]) diff++;
        if (diff > 1) return false;
    }
    return diff == 1;
}

// Utility to reverse a string into buffer
void reverseString(const char *src, char *dst) {
    int len = strlen(src);
    for (int i = 0; i < len; i++) {
        dst[i] = src[len - 1 - i];
    }
    dst[len] = '\0';
}

// BFS queue node
typedef struct Node {
    char word[MAX_WORD_LENGTH + 1];
    int steps;
} Node;

// Queue for BFS
Node queue[MAX_WORDS * MAX_WORDS];
int front = 0, rear = 0;
void enqueue(const char *word, int steps) {
    strcpy(queue[rear].word, word);
    queue[rear].steps = steps;
    rear++;
}
Node dequeue() {
    return queue[front++];
}
bool isEmpty() {
    return front == rear;
}

int findYulMyungPaths(const char *yul, const char *myung, char **wordList, int wordListSize) {
    // Check if myung exists in wordList or its reverse does
    bool exists = false;
    char rev[MAX_WORD_LENGTH + 1];
    reverseString(myung, rev);
    for (int i = 0; i < wordListSize; i++) {
        if (strcmp(wordList[i], myung) == 0 || strcmp(wordList[i], rev) == 0) {
            exists = true;
            break;
        }
    }
    if (!exists) return 0;

    // BFS
    front = rear = 0;
    int minStep = -1;
    int pathCount = 0;

    bool visited[MAX_WORDS] = {false};
    enqueue(yul, 0);

    while (!isEmpty()) {
        Node current = dequeue();
        if (minStep != -1 && current.steps > minStep) break;

        for (int i = 0; i < wordListSize; i++) {
            if (visited[i]) continue;

            if (isOneLetterDiff(current.word, wordList[i])) {
                if (strcmp(wordList[i], myung) == 0) {
                    if (minStep == -1) minStep = current.steps + 1;
                    if (current.steps + 1 == minStep) pathCount++;
                } else {
                    visited[i] = true;
                    enqueue(wordList[i], current.steps + 1);
                }
            } else {
                // check reverse
                char reversed[MAX_WORD_LENGTH + 1];
                reverseString(wordList[i], reversed);
                if (strcmp(reversed, current.word) == 0 || strcmp(reversed, myung) == 0) {
                    if (strcmp(wordList[i], myung) == 0 || strcmp(reversed, myung) == 0) {
                        if (minStep == -1) minStep = current.steps + 1;
                        if (current.steps + 1 == minStep) pathCount++;
                    } else {
                        visited[i] = true;
                        enqueue(wordList[i], current.steps + 1);
                    }
                }
            }
        }
    }

    return pathCount;
}
