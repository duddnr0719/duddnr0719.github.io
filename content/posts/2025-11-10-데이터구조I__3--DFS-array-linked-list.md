---
weight: 17
title: "3. DFS(array, linked list)"
date: 2025-11-10T12:00:00+09:00
categories: ["데이터구조I"]
draft: false
---

## 1. 개요
인접 행렬과 인접 연결리스트로 표현된 그래프에 대한 DFS를 구현한다.
### 2. 인접리스트 (지난주 실습문제와 비교)
(1) 정점의 수와 간선의 수를 입력하면 무작위로 그래프를 발생시키는 함수를 구현하라.
단, 정점 사이에 중복된 간선이 존재하지 않아야 한다. 생성된 그래프를 인접행렬로 표현하고 화면에 출력하고,
정점의 이름은 'A'로부터 시작하여 하나씩 증가시키도록 한다. 만들어진 연결 그래프에 깊이 우선 탐색을 적용하여 정점을 방문하는 순서를 출력한다.
```c
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define TRUE 1
#define FALSE 0
#define MAX_VERTICES 50

// DFS 수행 시, 정점의 방문 여부를 기록하는 배열
int visited[MAX_VERTICES];

// 그래프를 인접 행렬 방식으로 표현하는 구조체
typedef struct GraphType {
    int n; // 정점의 개수
    int adj_mat[MAX_VERTICES][MAX_VERTICES]; // 2차원 배열로 간선 정보를 저장
} GraphType;

// 그래프의 정점 개수와 인접 행렬을 초기화
void init(GraphType* g) {
    g->n = 0;
    for (int r = 0; r < MAX_VERTICES; r++)
        for (int c = 0; c < MAX_VERTICES; c++)
            g->adj_mat[r][c] = 0;
}

void insert_vertex(GraphType* g, int v) {
    if (((g->n) + 1) > MAX_VERTICES) {
        fprintf(stderr, "그래프: 정점의 개수 초과\n");
        return;
    }
    g->n++;
}

// 무방향 그래프이므로 양쪽 방향의 간선을 모두 표시
void insert_edge(GraphType* g, int start, int end) {
    if (start >= g->n || end >= g->n) {
        fprintf(stderr, "그래프: 정점 번호 오류\n");
        return;
    }
    g->adj_mat[start][end] = 1;
    g->adj_mat[end][start] = 1;
}

void print_adj_matrix(GraphType* g) {
    for (int i = 0; i < g->n; i++)
        printf("%c ", 'A' + i);
    printf("\n");
    for (int i = 0; i < g->n; i++) {
        printf("%c: ", 'A' + i);
        for (int j = 0; j < g->n; j++) {
            printf("%d ", g->adj_mat[i][j]);
        }
        printf("\n");
    }
}

// DFS 함수
void dfs_mat(GraphType* g, int v) {
    visited[v] = TRUE; // 현재 정점을 방문 처리
    printf("%c ", 'A' + v);

    // 현재 정점 v와 연결된 모든 정점을 확인
    for (int w = 0; w < g->n; w++) {
        // 간선이 존재하고, 아직 방문하지 않은 정점이라면 재귀 호출로 탐색을 이어감
        if (g->adj_mat[v][w] && !visited[w])
            dfs_mat(g, w);
    }
}

int main(void) {
    srand(time(NULL));
    GraphType* g;
    g = (GraphType*)malloc(sizeof(GraphType));
    init(g);

    int vertex, edge;
    printf("정점의 개수는? ");
    scanf("%d", &vertex);
    printf("랜덤 연결 그래프 생성\n");
    for (int i = 0; i < vertex; i++) {
        insert_vertex(g, i);
    }
    printf("간선의 개수는? ");
    scanf("%d", &edge);

    int count = 0;
    // 목표한 개수만큼 랜덤 간선을 생성
    while (count < edge) {
        int start = rand() % vertex;
        int end = rand() % vertex;
        
        // 자기 자신을 가리키는 간선과 중복 간선 방지
        if (start != end && g->adj_mat[start][end] == 0) {
            insert_edge(g, start, end);
            count++;
        }
    }

    print_adj_matrix(g);

    printf("\nDFS: ");
    for (int i = 0; i < vertex; i++) visited[i] = FALSE;
    dfs_mat(g, 0); 
    printf("\n");

    free(g);
    return 0;
}
```
### 실행 결과
![](/images/4c62be3f92fe3b7d.png)
(2) (1)에서 인접 행렬로 만들어진 연결그래프를 연결 리스트로 변환하여 연결 리스트의 구조를 출력하고 깊이 우선 탐색을 적용하여 정점을 방문하는 순서를 출력한다. (1)에서 정점을 방문한 순서와 (2)에서 정점을 방문한 순서를 비교해본다.
```c
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define MAX_VERTICES 50
#define TRUE 1
#define FALSE 0

// 방몬 기록을 위한 배열 정의
int visited[MAX_VERTICES];

// 인접 리스트 노드 구조체 정의
typedef struct GraphNode {
    int vertex;
    struct GraphNode* link;
} GraphNode;

// 그래프 구조체 정의
typedef struct GraphType {
    int n;
    GraphNode* adj_list[MAX_VERTICES];
} GraphType;

// 그래프 초기화
void init(GraphType* g) {
    g->n = 0;
    for (int i = 0; i < MAX_VERTICES; i++)
        g->adj_list[i] = NULL;
}

// 정점 추가
void insert_vertex(GraphType* g, int v) {
    if ((g->n) + 1 > MAX_VERTICES) {
        fprintf(stderr, "그래프: 정점의 개수 초과\n");
        return;
    }
    g->n++;
}

// 간선 추가 (양방향)
void insert_edge(GraphType* g, int start, int end) {
    if (start >= g->n || end >= g->n) {
        fprintf(stderr, "그래프: 정점 번호 오류\n");
        return;
    }
    // start -> end
    GraphNode* node = (GraphNode*)malloc(sizeof(GraphNode));
    node->vertex = end;
    node->link = g->adj_list[start];
    g->adj_list[start] = node;
    // end -> start (무방향)
    node = (GraphNode*)malloc(sizeof(GraphNode));
    node->vertex = start;
    node->link = g->adj_list[end];
    g->adj_list[end] = node;
}

// 인접 리스트 출력
void print_adj_list(GraphType* g) {
    for (int i = 0; i < g->n; i++) {
        printf("%c: ", 'A' + i);
        GraphNode* p = g->adj_list[i];
        while (p != NULL) {
            printf("%c ", 'A' + p->vertex);
            p = p->link;
        }
        printf("\n");
    }
}

// 깊이 우선 탑색 (DFS)
void dfs_list(GraphType* g, int v) {
    visited[v] = TRUE;
    printf("%c ", 'A' + v);
    GraphNode* p = g->adj_list[v];
    while (p != NULL) {
        if (!visited[p->vertex])
            dfs_list(g, p->vertex);
        p = p->link;
    }
}

int main(void) {
    srand(time(NULL));
    GraphType* g = (GraphType*)malloc(sizeof(GraphType));
    init(g);

    int vertex, edge;
    printf("정점의 개수는? ");
    scanf("%d", &vertex);
    printf("랜덤 연결 그래프 생성\n");
    for (int i = 0; i < vertex; i++) {
        insert_vertex(g, i);
    }
    printf("간선의 개수는? ");
    scanf("%d", &edge);

    int count = 0;
    // 목표한 개수만큼 랜덤 간선을 생성
    while (count < edge) {
        int start = rand() % vertex;
        int end = rand() % vertex;
        // 자기 자신, 중복 간선 방지
        int duplicate = FALSE;
        GraphNode* p = g->adj_list[start];
        while (p != NULL) {
            if (p->vertex == end) {
                duplicate = TRUE;
                break;
            }
            p = p->link;
        }
        if (start != end && !duplicate) {
            insert_edge(g, start, end);
            count++;
        }
    }

    print_adj_list(g);

    printf("\nDFS: ");
    for (int i = 0; i < vertex; i++) visited[i] = FALSE;
    dfs_list(g, 0);
    printf("\n");

    // 메모리 해제(생략 가능, 실제로는 각 리스트 노드도 free 필요)
    free(g);
    return 0;
}
```
### 실행 결과
![](/images/3021fe0f8c409bb5.png)
### 3. 아래와 같이 7X7 인접행렬을 보이고 있다. 
인접행렬과 인접리스트를 구현하여 출력하고, 정점 (0,0)에서 시작하여 DFS를 이용하여 정점 방문하는 순서를 출력한다. 인접 행렬로 만들어진 연결그래프를 DFS적용했을 때 정점 방문 순서와 인접리스트로 만들어진 연결그래프를 이용하여 DFS적용했을 때 정점 방문 순서와 비교해본다.
```c
#include <stdio.h>
#include <stdlib.h>

#define MAX_VERTICES 50
#define TRUE 1
#define FALSE 0

// 인접 리스트 구조체 정의
typedef struct GraphNode {
    int vertex;
    struct GraphNode* link;
} GraphNode;

// 그래프 구조체 정의
typedef struct GraphType {
    int n; 
    GraphNode* adj_list[MAX_VERTICES];
} GraphType;

// 방문 기록을 위한 배열 정의
int visited[MAX_VERTICES];

// 그래프 초기화
void init(GraphType* g) {
    g->n = 0;
    for (int i = 0; i < MAX_VERTICES; i++)
        g->adj_list[i] = NULL;
}

// 정점 삽입
void insert_vertex(GraphType* g) {
    if ((g->n) + 1 > MAX_VERTICES) {
        fprintf(stderr, "그래프: 정점의 개수 초과\n");
        return;
    }
    g->n++;
}

// 간선 삽입 (단방향)
void insert_edge(GraphType* g, int start, int end) {
    if (start >= g->n || end >= g->n) {
        fprintf(stderr, "그래프: 정점 번호 오류\n");
        return;
    }

    GraphNode* node = (GraphNode*)malloc(sizeof(GraphNode));
    node->vertex = end;
    node->link = g->adj_list[start];
    g->adj_list[start] = node;
}

// 인접 리스트 출력
void print_adj_list(GraphType* g) {
    for (int i = 0; i < g->n; i++) {
        printf("정점 %c -> ", 'A' + i);
        GraphNode* p = g->adj_list[i];
        if (p == NULL) {
            printf("NULL");
        }
        while (p != NULL) {
            printf("%c ", 'A' + p->vertex);
            if(p->link != NULL) printf("-> ");
            p = p->link;
        }
        printf("\n");
    }
}

// 깊이 우선 탐색 (DFS)
void dfs_list(GraphType* g, int v) {
    visited[v] = TRUE;
    printf("%c -> ", 'A' + v); // 방문한 정점을 문자로 출력
    
    GraphNode* p = g->adj_list[v];
    while (p != NULL) {
        if (!visited[p->vertex])
            dfs_list(g, p->vertex);
        p = p->link;
    }
}

// 그래프 메모리 해제 함수
void free_graph(GraphType* g) {
    for (int i = 0; i < g->n; i++) {
        GraphNode* p = g->adj_list[i];
        while (p != NULL) {
            GraphNode* removed = p;
            p = p->link;
            free(removed);
        }
    }
    free(g);
}

int main(void) {
    // 그래프 정의
    GraphType* g = (GraphType*)malloc(sizeof(GraphType));
    init(g);

    // 주어진 인접 행렬 정의
    int adjMatrix[7][7] = {
        {0, 1, 1, 1, 1, 1, 1},
        {1, 0, 0, 0, 0, 0, 1},
        {1, 1, 1, 0, 1, 1, 1},
        {0, 0, 1, 0, 1, 0, 0},
        {0, 0, 1, 1, 1, 1, 0},
        {0, 0, 1, 0, 0, 1, 1},
        {0, 1, 1, 1, 1, 1, 0}
    };
    // 정점의 개수 설정
    int vertex_count = 7;

    // 인접 행렬을 인접 리스트로 변환
    for (int i = 0; i < vertex_count; i++) {
        insert_vertex(g);
    }

    // 간선 삽입 연산 실행
    for (int i = 0; i < vertex_count; i++) {
        for (int j = 0; j < vertex_count; j++) {
            if (adjMatrix[i][j] == 1) {
                insert_edge(g, i, j);
            }
        }
    }
    

    // 인접 리스트 출력
    print_adj_list(g);

    printf("## 깊이 우선 탐색 (DFS) 결과\n\n");
    printf("방문 순서: ");

    // 방문 기록 초기화
    for (int i = 0; i < g->n; i++) {
        visited[i] = FALSE;
    }
    dfs_list(g, 0); 
    printf("\n");

    free_graph(g); 

    return 0;
}
```
### 실행 결과
![](/images/d034c210a8bbbbeb.png)
