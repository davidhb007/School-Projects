#include <stdio.h>
#include <_types.h>
#include <stdlib.h>
#include <stdbool.h>
#include <pthread.h>
#include <sys/queue.h>
#include <unistd.h>

#define NUMBER_OF_POSITIONS 10

// Declare Mutexes and Condition variables
static pthread_mutex_t mutex;
static pthread_cond_t initial_group_done = PTHREAD_COND_INITIALIZER;
static pthread_cond_t position_free = PTHREAD_COND_INITIALIZER;

// declare the structure of the requests for the DBMS
typedef struct
{
    int user, group, requestPos, arrivalTime, duration;
} request;

void showRequest(request *r)
{
    printf("User %d from Group %d requesting postition %d at time %d for %d sec \n",
           r->user, r->group, r->requestPos, r->arrivalTime, r->duration);
}

// Structuring array of size 30 to store requests and implement as queue
static request requestArray[30];
static int front = 0;
static int rear = -1;
int itemCount = 0;

static void push(request arg)
{
    if (itemCount < 30)
    {
        requestArray[++rear] = arg;
        itemCount++;
    }
}

static request *pop()
{
    if (itemCount > 0)
    {
        request *r = &requestArray[front];
        front++;
        itemCount--;
        return r;
    }
    return NULL;
}
// end of queue structuring

int group1req = 0; // store total requests belonging to group 1
int group2req = 0; // stroe total requests belonging to group 2

// Struct containing information about initial group with access to the dbms
typedef struct
{
    int group, count;
} initialGroup;

static initialGroup ig;

// Declare static variables shared by all threads
static int waitForGroupCount, waitForLockedPos, excecuted = 0;
static int accessedBy[10] = {0};
static int posWaitCount[10] = {0};
static bool counter = false;

// Thread Function to access the dbms
void *accessDbms(void *void_request_pointer)
{
    // Enter critical section 1
    pthread_mutex_lock(&mutex);
    request req = *(request *)void_request_pointer;
    printf("User %d from Group %d arrives to the DBMS\n", req.user, req.group);

    if (req.group != ig.group && ig.count != 0 && counter == false)
    {
        waitForGroupCount++;
        printf("User %d is waiting due to its group\n", req.user);
        pthread_cond_wait(&initial_group_done, &mutex);
    }
    if (accessedBy[req.requestPos - 1] != 0)
    {
        posWaitCount[req.requestPos - 1]++;
        waitForLockedPos++;
        printf("User %d is waiting: position %d of the database is being used by user %d\n",
               req.user, req.requestPos, accessedBy[req.requestPos - 1]);
        pthread_cond_wait(&position_free, &mutex);
    }
    printf("User %d is accessing the position %d of the database for %d second(s)\n",
           req.user, req.requestPos, req.duration);

    accessedBy[req.requestPos - 1] = req.user;

    pthread_mutex_unlock(&mutex);

    // Exit critical section 1
    sleep(req.duration);
    // Enter critical section 2

    pthread_mutex_lock(&mutex);
    printf("User %d finished its execution\n", req.user);
    accessedBy[req.requestPos - 1] = 0;
    excecuted++;
    if (posWaitCount[req.requestPos - 1] > 0)
    {
        pthread_cond_signal(&position_free);
        posWaitCount[req.requestPos - 1]--;
    }

    if (excecuted == ig.count && req.group == 1)
    {
        printf("All users from Group %d finished their execution\n", ig.group);
        printf("The users from Group 2 start their execution\n");
        counter = true;
        pthread_cond_broadcast(&initial_group_done);
    }
    else if (excecuted == ig.count && req.group == 2)
    {
        printf("All users from Group %d finished their execution\n", ig.group);
        printf("The users from Group 1 start their execution\n");
        counter = true;
        pthread_cond_broadcast(&initial_group_done);
    }

    pthread_mutex_unlock(&mutex); // Exit critical section 2
    return NULL;
}

int main()
{
    ig.group = 1; // Initialize the dbms access for group 1 by default
    ig.count = 0; // Initialize the initial group request count to 0
    scanf("%d", &ig.group);
    int a, b, c, d;
    int t = 0;

    // Take requests info from stdin and store each in the propper struct
    int reqCount = 0;
    while (scanf("%d %d %d %d \n", &a, &b, &c, &d) != EOF)
    {
        if (a == 1)
        {
            group1req++; //Record that request belongs to Group1
            if (a == ig.group)
            {
                ig.count++;
            }
        }
        else if (a == 2)
        {
            group2req++; //Record that request belongs to Group2
            if (a == ig.group)
            {
                ig.count++;
            }
        }
        else
        {
            continue;
        } //If group is not valid, ignore request and continue looping
        reqCount++;
        request r = {reqCount, a, b, c, d};
        push(r);
    }

    // Initialize mutex
    pthread_mutex_init(&mutex, NULL);
    // Declare array of pthreads containing the same amount of requests
    pthread_t threads[reqCount];
    // Start threads to act as individual requests to the dbms
    for (int i = 0; i < reqCount; i++)
    {
        sleep(requestArray[i].arrivalTime);
        pthread_create(&threads[i], NULL, accessDbms, (void *)&requestArray[i]);
    }

    for (int i = 0; i < reqCount; i++)
    {
        pthread_join(threads[i], NULL);
    }

    printf("Total Requests:\n");
    printf("\tGroup 1: %d\n\tGroup 2: %d\n", group1req, group2req);

    printf("Requests that waited:\n");
    printf("\tDue to its group: %d\n\tDue to a locked position: %d\n",
           waitForGroupCount, waitForLockedPos);

    return 0;
}