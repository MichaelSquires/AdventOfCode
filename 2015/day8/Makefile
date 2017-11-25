CFLAGS=-Wall -Werror
TARGET=day8
SRCS=main.c fileops.c

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
