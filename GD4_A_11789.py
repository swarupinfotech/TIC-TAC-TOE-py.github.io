# This tic tac toe game is developed by Swarup Mahato
import copy
import sys
import pygame
import random
import numpy as np 

from constants import *
from tkinter import messagebox
import tkinter as tk

# --- PYGAME SETUP ---
pygame.init() # Inisialisasi
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('TIC TAC TOE AI') 
screen.fill( BG_COLOR ) # Background color

# --- CLASSES ---
class Board :
    def __init__(self) : 
        self.squares = np.zeros((ROWS, COLS)) 
        self.empty_sqrs = self.squares # [squares]
        self.marked_sqrs = 0 # Inisialisasi Mengosongkan Board
        for row in range(ROWS):
            for col in range(COLS):
                self.empty_sqrs[row][col] = 0
    
    def final_state(self, show=False):
        '''
        Return 0 Jika Belum ada yang menang
        Return 1 Jika Player 1 Menang
        Return 2 Jika Player 2 Menang
        '''
        # Players Wins
        for col in range(COLS): 
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0: 
                if show:
                    color = CIRC_COLOR if self.squares[0][col] == 2 else CROSS_COLOR  
                    iPos = (col * SQSIZE + SQSIZE // 2, 20) 
                    fPos = (col * SQSIZE + SQSIZE // 2, HEIGHT - 20)
                    pygame.draw.line( screen, color, iPos, fPos, LINE_WIDTH) 
                return self.squares[0][col]
            
       
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] !=0: # Koordinat Ketika Kemenangan Terjadi Secara Horizontal
                if show:
                    color = CIRC_COLOR if self.squares[row][0] == 2 else CROSS_COLOR # Menampilkan Warna Ketika Kemenangan Horizontal
                    iPos = (20, row * SQSIZE + SQSIZE // 2)
                    fPos = (WIDTH - 20, row * SQSIZE + SQSIZE // 2)
                    pygame.draw.line( screen, color, iPos, fPos, LINE_WIDTH) # Menggambar Garis Kemenangan Secara Horizontal
                return self.squares[row][0]
        
        # Desc Diagonal
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0: # Koordinat Ketika Kemenangan Terjadi Secara Desc Diagonal
            if show:
                color = CIRC_COLOR if self.squares[1][1] == 2 else CROSS_COLOR # Menampilkan Warna Ketika Kemenangan Desc Diagonal
                iPos = (20, 20)
                fPos = (WIDTH - 20, HEIGHT - 20)
                pygame.draw.line( screen, color, iPos, fPos, CROSS_WIDTH) # Menggambar Garis Kemenangan Secara Desc Diagonal
            return self.squares[1][1]
        
        # Asc Diagonal
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0: # Koordinat Ketika Kemenangan Terjadi Secara Desc Diagonal
            if show:
                color = CIRC_COLOR if self.squares[1][1] == 2 else CROSS_COLOR # Menampilkan Warna Ketika Kemenangan Asc Diagonal
                iPos = (20, HEIGHT - 20)
                fPos = (WIDTH - 20, 20)
                pygame.draw.line( screen, color, iPos, fPos, CROSS_WIDTH) # Menggambar Garis Kemenangan Secara Asc Diagonal
            return self.squares[1][1]
        
        # no win yet
        return 0
    
    def mark_sqr(self, row, col, player): # Menandai Kotak pada Koordinat Pemain
        self.squares[row][col] = player
        self.marked_sqrs += 1
    def empty_sqr(self, row, col): # Mengecek Kotak yang masih kosong
        return self.squares[row][col] == 0
    def get_empty_sqrs(self): # Mengembalikan Daftar Kotak yang masih kosong pada papan
        empty_sqrs = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_sqr(row, col):
                    empty_sqrs.append((row, col))
        return empty_sqrs
    
    def isfull(self): # Mengembalikan true ketika semua kotak pada papan telah terisi
        return self.marked_sqrs == 9
    
    def isempty(self): # Mengembalikan true ketika tidak ada kotak yang terisi
        return self.marked_sqrs == 0
# ---- KELAS AI ----
class AI:
    def __init__(self, level=1, player=2): # Inisialisasi Objek yang ada pada game
        self.level = level
        self.player = player

    # --- RANDOM ---
    def rnd(self, board): # memilih langkah secara acak dari kotak yang masih kosong pada papan permainan
        empty_sqrs = board.get_empty_sqrs()
        idx = random.randrange(0, len(empty_sqrs))

        return empty_sqrs[idx]
    # --- MINIMAX ---
    def minimax(self, board, maximizing): 
        # Metode Implementasi Algoritma Minimax untuk mengevaluasi semua langkah yang mungkin dan memilih langkah terbaik
        # terminal case
        case = board.final_state()

        # Kemungkinan Jika Player 1 Menang
        if case == 1:
            return 1, None
        # Kemungkinan Jika Player 2 Menang
        if case == 2:
            return -1, None
        # Kemungkinan Jika Kedua Player Draw
        elif board.isfull():
            return 0, None
        
        if maximizing:
            max_eval = -100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)
            # Mencari Langkah Terbaik yang harus diambil oleh AI
            return max_eval, best_move
        
        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()
            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)
            # Mencari Langkah Terbaik yang harus diambil oleh AI
            return min_eval, best_move
        
    # --- MAIN EVAL ---
    def eval(self, main_board):
        if self.level == 0: # Jika tingkatan Level AI 0
            eval = 'random' # Langkah yang dilakukan AI akan random
            move = self.rnd(main_board)
        else: # Jika tingkatan Level AI 1
            eval, move = self.minimax(main_board, False) # AI Menggunakan Algoritma Minimax

        print(f'AI has choosen to mark the square in pos {move} with an eval of: {eval}')
        
        return move # Mengembalikan langkah Terbaik yang diambil oleh AI
    
class Game:
    def __init__(self):  
        self.board = Board() # Inisialisasi Board
        self.ai = AI() # Inisialisasi AI
        self.player = 1 # Inisialisasi Player
        self.gamemode = 'ai' # Inisialisasi Mode Game Awal Menjadi AI
        self.running = True 
        self.show_lines() # Inisialisasi Kemunculan Garis saat kemenangan

    def show_lines(self): # Logika Penggambaran Garis ketika kemenangan
        screen.fill(BG_COLOR)

        # Garis Vertical
        pygame.draw.line(screen, LINE_COLOR, (SQSIZE, 0), (SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (WIDTH-SQSIZE, 0), (WIDTH - SQSIZE, HEIGHT), LINE_WIDTH)

        # Garis Horizontal
        pygame.draw.line(screen, LINE_COLOR, (0, SQSIZE), (WIDTH, SQSIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT - SQSIZE), (WIDTH, HEIGHT - SQSIZE), LINE_WIDTH)
    
    def draw_fig(self, row, col): # Metode Untuk Menggambar Simbol pada Kotak Tertentu
        if self.player == 1: # Logika Penggambaran CROSS
            # DESC LINE
            start_desc = (col * SQSIZE + OFFSET, row * SQSIZE + OFFSET)
            end_desc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)
            # ASC LINE
            start_asc = (col * SQSIZE + OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            end_asc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)
        
        elif self.player == 2: # Logika Penggambaran CIRCLE
            center = (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2)
            pygame.draw.circle(screen, CIRC_COLOR, center, RADIUS, CIRC_WIDTH)

    # --- BUTTON METHODS ---
    def reset(self): # Fungsi Pembuatan Tombol Reset
        root = tk.Tk()
        root.withdraw()
        result = messagebox.askquestion("Restart Game", "Do you want to restart the game? ")
        if result == 'yes':
            self.__init__() # Fungsi Reset Menjadi Seperti Semula
    
    def change_gamemode(self): # Fungsi untuk mengubah game mode
        root = tk.Tk()
        root.withdraw()

        if self.gamemode == 'pvp' : # Logika Pengubahan Game Mode dari PVP ke AI
            result = messagebox.askquestion("Change Mode", "Do you want to Change to AI Mode? ")
            if result == 'yes':
                self.gamemode = 'ai'
        
        else: # Logika Pengubahan Game Mode dari AI ke PVP
            result = messagebox.askquestion("Change Mode", "Do you want to Change to PVP Mode? ")
            if result == 'yes':
                self.gamemode = 'pvp'

    def isover(self): # Metode untuk mengecek apakah permainan sudah selesai 
        return self.board.final_state(show=True) != 0 or self.board.isfull()
    
    # --- OTHER METHODS ---
    def make_move(self, row, col): # Metode untuk membuat langkah pada kotak tertentu dalam permainan
        self.board.mark_sqr(row, col, self.player)
        self.draw_fig(row, col)
        self.next_turn()
    
    def next_turn(self): # Metode untuk beralih ke pemain berikutnya
        self.player = self.player % 2 + 1

def main(): # Fungsi MAIN / UTAMA
    # --- OBJECTS ---
    game = Game() # Inisialisasi Objek
    board = game.board
    ai = game.ai
    
    # --- MAIN LOOP ---
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Logika ketika ingin keluar dari game
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:# Logika keyboard ketika ingin mengubah gamemode atau melakukan reset
                # G - gamemode
                if event.key == pygame.K_g: # Logika Mengubah Game Mode
                    game.change_gamemode()
                # R - restart
                if event.key == pygame.K_r: # Logika Reset Game
                    game.reset() # Penggilan Fungsi Untuk Reset Game
                    board = game.board
                    ai = game.ai # Game diset menjadi AI Ketika dilakukan reset 
                # 0 - random ai
                if event.key == pygame.K_0: 
                    ai.level = 0
                # 1 - random ai
                if event.key == pygame.K_1: 
                    ai.level = 1
            if event.type == pygame.MOUSEBUTTONDOWN:  
                pos = event.pos
                row = pos[1] // SQSIZE
                col = pos[0] // SQSIZE

                # Human Mark SQR
                if board.empty_sqr(row, col) and game.running: 
                    game.make_move(row, col)
                    if game.isover(): 
                        game.running = False
       
        if game.gamemode == 'ai' and game.player == ai.player and game.running:
            pygame.display.update() 
            row, col = ai.eval(board)
            game.make_move(row, col)
            if game.isover(): 
                game.running = False
            
        pygame.display.update() 

main()

