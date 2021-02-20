CC=gcc
CFLAGS=-W -Wall -lpthread -g

EXEC=bin

OBJ_DIR = obj
SRC_DIR = src

MKDIR_P = mkdir -p
OUT_DIR = $(OBJ_DIR)

SRC:= $(wildcard $(SRC_DIR)/*.c)
OBJ:= $(SRC:$(SRC_DIR)/%.c=$(OBJ_DIR)/%.o)

.PHONY: clean directories all

all: directories $(EXEC)

directories: ${OUT_DIR}

${OUT_DIR}:
	${MKDIR_P} ${OUT_DIR}

$(OBJ_DIR)/%.o: $(SRC_DIR)/%.c 
	@echo "[I] Making $@"
	$(CC)  -c  $< -o $@ $(CFLAGS)

$(EXEC): $(OBJ)
	@echo "[I] Making $@"
	$(CC)  $(OBJ) -o $@ $(CFLAGS)

clean:
	rm -rf $(OBJ_DIR)
	rm -f $(EXEC)
