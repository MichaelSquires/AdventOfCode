CFLAGS=-Wall -Werror
TARGET=day12
SRCS=main.c fileops.c json.c

all: $(TARGET)

debug: CFLAGS += -DDEBUG
debug: $(TARGET)

OBJS = $(SRCS:.c=.o)

$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) -o $(TARGET) $(OBJS)

.c.o:
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	$(RM) $(OBJS) $(TARGET)

.PHONY: clean
