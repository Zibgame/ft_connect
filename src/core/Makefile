NAME_MAIN = ft_connect
NAME_MONITOR = monitor

PYINSTALLER = ~/.local/bin/pyinstaller

SRC_MAIN = ft_connect[REBOOT].py
SRC_MONITOR = monitor.py

ROOT_DIR = ../..
CORE_DIR = .

BUILD_DIR = .build
DIST_DIR = .dist
SPEC_DIR = .spec

BIN_MAIN = $(CORE_DIR)/$(NAME_MAIN)
BIN_MONITOR = $(ROOT_DIR)/$(NAME_MONITOR)

BINS = $(BIN_MAIN) $(BIN_MONITOR)

GREEN = \033[0;32m
BLUE  = \033[0;34m
RED   = \033[0;31m
RESET = \033[0m

all: banner $(BINS)
	@echo "$(GREEN)✔ Build terminé$(RESET)"

banner:
	@echo "$(BLUE)"
	@echo "===================================="
	@echo "   FT_CONNECT – PYINSTALLER BUILD"
	@echo "===================================="
	@echo "$(RESET)"

$(BIN_MAIN):
	@echo "$(BLUE)[+] Build $(NAME_MAIN)$(RESET)"
	@$(PYINSTALLER) \
		--onefile \
		--name $(NAME_MAIN) \
		--distpath $(DIST_DIR) \
		--workpath $(BUILD_DIR) \
		--specpath $(SPEC_DIR) \
		$(SRC_MAIN)
	@mv $(DIST_DIR)/$(NAME_MAIN) $(BIN_MAIN)
	@chmod 755 $(BIN_MAIN)
	@echo "$(GREEN)✔ $(BIN_MAIN) (755)$(RESET)"

$(BIN_MONITOR):
	@echo "$(BLUE)[+] Build $(NAME_MONITOR)$(RESET)"
	@$(PYINSTALLER) \
		--onefile \
		--name $(NAME_MONITOR) \
		--distpath $(DIST_DIR) \
		--workpath $(BUILD_DIR) \
		--specpath $(SPEC_DIR) \
		$(SRC_MONITOR)
	@mv $(DIST_DIR)/$(NAME_MONITOR) $(BIN_MONITOR)
	@chmod 755 $(BIN_MONITOR)
	@echo "$(GREEN)✔ $(BIN_MONITOR) (755)$(RESET)"

clean:
	@echo "$(RED)[-] Nettoyage build$(RESET)"
	@rm -rf $(BUILD_DIR)

fclean: clean
	@echo "$(RED)[-] Nettoyage complet$(RESET)"
	@rm -rf $(DIST_DIR) $(SPEC_DIR) $(BINS)

re: fclean all

.PHONY: all clean fclean re banner
