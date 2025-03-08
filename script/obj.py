import pygame
from script.setting import *

#Criação de Arquivo que vai receber imagens e posições,
# para poderem ser desenhados na tela

class Obj(pygame.sprite.Sprite):
    
    def __init__(self, img, pos, groups, size=None):
        super().__init__(groups)  # Inicializa a classe pai com os grupos
        self.image = pygame.image.load(img).convert_alpha()  # Carrega a imagem com suporte a transparência
        
        if size:
            self.image = pygame.transform.scale(self.image, size)  # Redimensiona a imagem se um tamanho for especificado
        self.rect = self.image.get_rect(topleft=pos)  # Define o retângulo da imagem na posição especificada
        self.visible = True  # Define a visibilidade padrão como True
    
    def update(self):
        """Atualiza a visibilidade do objeto."""
        if self.visible:
            self.image.set_alpha(255)  # Totalmente visível
        else:
            self.image.set_alpha(0)  # Invisível

    def draw(self, surface):
        """Desenha o objeto na superfície, se visível."""
        if self.visible:
            surface.blit(self.image, self.rect.topleft)  # Desenha a imagem na posição do retângulo

class Fade(Obj):
    """Classe para criar um efeito de desvanecimento."""
    
    def __init__(self, color):
        self.image = pygame.Surface((BASE_WIDTH, BASE_HEIGHT)).convert_alpha()  # Superfície para o efeito de fade
        self.image.fill(color)  # Preenche a superfície com a cor especificada
        self.image_alpha = 255  # Opacidade inicial
        self.speed_alpha = 5  # Velocidade de desvanecimento

    def draw(self, display):
        """Desenha a superfície de fade na tela."""
        display.blit(self.image, (0, 0))

    def update(self):
        """Atualiza a opacidade da superfície de fade."""
        if self.image_alpha > 1:
            self.image_alpha -= self.speed_alpha  # Reduz a opacidade

        self.image.set_alpha(self.image_alpha)  # Define a opacidade da superfície


class Text(pygame.sprite.Sprite):
    """Classe para criar e renderizar texto na tela."""
    
    def __init__(self, font_size, text, color, pos, groups):
        super().__init__(groups)  # Inicializa a classe pai com os grupos
        
        self.color = color  # Define a cor do texto
        
        # Renderizando um texto na Tela
        self.font = pygame.font.Font("assets/font/Primitive.ttf", font_size)  # Carrega a fonte com o tamanho especificado
        self.image = self.font.render(text, True, self.color)  # Renderiza o texto
        self.rect = self.image.get_rect(topleft=pos)  # Define o retângulo da imagem na posição especificada
        
    def update_text(self, text):
        """Atualiza o texto exibido."""
        self.image = self.font.render(text, True, self.color)  # Renderiza o novo texto


class Char(Obj):
    """Classe para representar um personagem no jogo."""
    
    def __init__(self, image_selected, image_unselected, pose, position, pose_position, size_selected, size_unselected, pose_size, status_image, status_position):
        self.image_selected = self.load_image(image_selected, size_selected)  # Carrega a imagem selecionada
        self.image_unselected = self.load_image(image_unselected, size_unselected)  # Carrega a imagem não selecionada
        self.pose = self.load_image(pose, pose_size)  # Carrega a pose do personagem
        self.position = position  # Posição do personagem
        self.pose_position = pose_position  # Posição da pose do personagem
        self.status_image = self.load_image(status_image, None)  # Carrega a imagem da placa de status
        self.status_position = status_position  # Posição da placa de status
        self.visible = True  # Define visibilidade padrão como True

    def load_image(self, img_path, size):
        """Carrega uma imagem a partir do caminho fornecido."""
        try:
            image = pygame.image.load(img_path).convert_alpha()  # Carrega a imagem com suporte a transparência
            return pygame.transform.scale(image, size) if size else image  # Redimensiona se o tamanho for especificado
        except pygame.error as e:
            print(f"Erro ao carregar a imagem {img_path}: {e}")  # Exibe erro caso a imagem não carregue
            return None  # Retorna None se a imagem falhar ao carregar

    def draw(self, surface, selected):
        """Desenha o personagem na superfície especificada."""
        if self.visible:  # Verifica se o personagem está visível
            if selected:
                surface.blit(self.image_selected, self.position)  # Desenha a imagem selecionada
                surface.blit(self.pose, self.pose_position)  # Desenha a pose do personagem
                surface.blit(self.status_image, self.status_position)  # Desenha a placa de status
            else:
                surface.blit(self.image_unselected, self.position)  # Desenha a imagem não selecionada

    def set_visible(self, visible):
        """Define a visibilidade do personagem."""
        self.visible = visible
  
        
class Map(Obj):
    """Classe para representar uma área do mapa."""
    
    def __init__(self, image_selected, area_completed, position, cursor_position):
        self.image_selected = self.load_image(image_selected)  # Carrega a imagem quando a área está selecionada
        self.area_completed = self.load_image(area_completed)  # Carrega a imagem quando a área está completada
        self.position = position  # Posição da área no mapa
        self.cursor_position = cursor_position  # Posição do cursor sobre a área
        self.visible = True  # Define visibilidade padrão como True

    def load_image(self, img_path):
        """Carrega uma imagem a partir do caminho fornecido."""
        try:
            image = pygame.image.load(img_path).convert_alpha()  # Carrega a imagem com suporte a transparência
            return image  # Retorna a imagem carregada
        except pygame.error as e:
            print(f"Erro ao carregar a imagem {img_path}: {e}")  # Exibe erro caso a imagem não carregue
            return None  # Retorna None se a imagem falhar ao carregar

    def draw(self, surface, selected):
        """Desenha a área do mapa na superfície especificada."""
        if self.visible:  # Verifica se a área está visível
            if selected:
                surface.blit(self.image_selected, self.position)  # Desenha a imagem selecionada
            else:
                surface.blit(self.area_completed, self.position)  # Desenha a imagem completada

    def set_visible(self, visible):
        """Define a visibilidade da área."""
        self.visible = visible
  
        
class Ground(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((0, 255, 0))  # Cor verde para o chão
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, surface):
        surface.blit(self.image, self.rect)  # Desenha a imagem do chão na tela


class Hud(Obj):
    """Classe para representar o painel de Dados do Jogador: XP, Ouro, Vidas e Life."""
    
    def __init__(self, image_path, position, groups, size=(200, 200)):
        super().__init__(image_path, position, groups, size)
        self.size = size

        # Carregando imagens de fundo e contorno
        self.xp_bK = pygame.image.load("assets/charsSprite/player/Hud/Hud_Char_Fundo_XP.png").convert_alpha()
        self.xp_bar = pygame.image.load("assets/charsSprite/player/Hud/Hud_Char_Barra_XP.png").convert_alpha()
        self.hud_bk = pygame.image.load("assets/charsSprite/player/Hud/Hud_Char_Fundo.png").convert_alpha()
        self.life_bar = pygame.image.load("assets/charsSprite/player/Hud/Hud_Life00PV.png").convert_alpha()
        self.contour_image = pygame.image.load("assets/charsSprite/player/Hud/Hud_Char_Contorno.png").convert_alpha()

        # Escalando as imagens para o tamanho do HUD
        self.scaled_xp_background = pygame.transform.scale(self.xp_bK, size)
        self.scaled_xp_bar = pygame.transform.scale(self.xp_bar, size)
        self.scaled_background = pygame.transform.scale(self.hud_bk, size)
        self.scale_life_bar = pygame.transform.scale(self.life_bar, size)
        self.scaled_contour = pygame.transform.scale(self.contour_image, size)
        
       # Carregando imagens de pontos de vida
        self.life_images = self.load_life_images()

        # Criando Surface principal para compor todas as camadas
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=position)

        # Inicializando valores de vida e XP
        self.life = 25  # Valor inicial de vida (máximo)
        self.max_life = 25
        self.xp = 0
        self.max_xp = 100
        self.live = 3  # Número inicial de vidas
        self.gold = 0  # Inicializando o valor do ouro 

    def load_life_images(self):
        """Carrega todas as imagens de vida automaticamente."""
        images = []
        for i in range(26):  # De 0 a 25
            path = f"assets/charsSprite/player/Hud/Hud_Life{i:02d}PV.png"
            try:
                image = pygame.image.load(path).convert_alpha()
                scaled_image = pygame.transform.scale(image, (self.size[0] // 1, self.size[1] // 1))
                images.append(scaled_image)
            except pygame.error as e:
                print(f"Erro ao carregar {path}: {e}")
                images.append(None)  # Adiciona None caso a imagem não seja encontrada
        return images

    def update_life(self, life):
        """Atualiza os pontos de sangue (Life) do jogador."""
        self.life = max(0, min(life, self.max_life))  # Garante que o valor esteja entre 0 e max_life

    def update_live(self, live):
        """Atualiza o número de vidas (Live) do jogador."""
        self.live = max(0, live)  # Garante que o número de vidas seja >= 0

    def update_xp(self, xp):
        """Atualiza o XP do jogador."""
        self.xp = max(0, min(xp, self.max_xp))  # Garante que o valor esteja entre 0 e max_xp
        
    def update_gold(self, gold):
        """Atualiza o ouro do jogador (máximo 9999)."""
        self.gold = max(0, min(gold, 9999))  # Garante que o valor esteja entre 0 e 9999

    def compose_hud(self):
        """Compoe as camadas do HUD."""
        self.image.fill((0, 0, 0, 0))  # Reseta o Surface (transparente)

        # Desenhando o fundo do XP
        self.image.blit(self.scaled_xp_background, (0, 0))

        # Desenhando a barra de XP proporcional
        xp_width = int((self.xp / self.max_xp) * self.size[0])
        xp_bar_rect = pygame.Rect(0, self.size[1] - 20, xp_width, 10)  # Exemplo de barra
        self.image.blit(self.scaled_xp_bar, xp_bar_rect, xp_bar_rect)

        # Desenhando a imagem correspondente à vida
        if self.life_images[self.life]:  # Verifica se a imagem existe
            life_image = self.life_images[self.life]
            self.image.blit(life_image, (0, 0))  # Alinhado no canto superior esquerdo

            # Desenhando o fundo principal do HUD
            self.image.blit(self.scaled_background, (0, 0))

            # Desenhando o contorno por cima de tudo
            self.image.blit(self.scaled_contour, (0, 0))
            
            # Exibindo o contador de ouro.
            font = pygame.font.Font(None, 25)
            gold_text = font.render(f"{self.gold:04d}", True, (BLACK_COLOR))  # Cor dourada para ouro
            self.image.blit(gold_text, (175, 40))  # Posição do contador de ouro no HUD

            # Exemplo de exibição do número de vidas (Live)
            font = pygame.font.Font(None, 30)
            live_text = font.render(f"{self.live}", True, (BLACK_COLOR))
            self.image.blit(live_text, (155, 60))  # Posição no HUD

    def update(self):
        """Atualiza o HUD."""
        self.compose_hud()  # Atualiza a composição do HUD


class Player(Obj):
    """Classe para representar o jogador no jogo Guardiões de Pindorama."""
    
    def __init__(self, image_path, position, groups, size=(200, 200)):
        super().__init__(image_path, position, groups, size)
        self.size = size
        self.original_image = pygame.image.load("assets/charsSprite/player/indigenaM/R0.png").convert_alpha()
        self.image = pygame.transform.scale(self.original_image, size)
        self.rect = self.image.get_rect(topleft=position)
        self.in_hole = False
        self.facing_right = True
        self.is_dead = False

        self.vel = 5
        self.grav = 0.5
        self.jump_power = -15  # Velocidade inicial para o pulo
        self.is_jumping = False  # Verifica se está pulando
        self.on_ground = False  # Verifica se está no chão

        # Flags de direção e estado de movimento
        self.right = False
        self.left = False

        self.ticks = 0
        self.img = 0
        
        self.animations = {
            "idle": [pygame.transform.scale(pygame.image.load(f"assets/charsSprite/player/indigenaM/R0.png"), size),
                     pygame.transform.scale(pygame.image.load(f"assets/charsSprite/player/indigenaM/R1.png"), size)],
            "walk": [pygame.transform.scale(pygame.image.load(f"assets/charsSprite/player/indigenaM/M0.png"), size),
                     pygame.transform.scale(pygame.image.load(f"assets/charsSprite/player/indigenaM/M1.png"), size),
                     pygame.transform.scale(pygame.image.load(f"assets/charsSprite/player/indigenaM/M2.png"), size),
                     pygame.transform.scale(pygame.image.load(f"assets/charsSprite/player/indigenaM/M3.png"), size),
                     pygame.transform.scale(pygame.image.load(f"assets/charsSprite/player/indigenaM/M4.png"), size),
                     pygame.transform.scale(pygame.image.load(f"assets/charsSprite/player/indigenaM/M5.png"), size),
                     pygame.transform.scale(pygame.image.load(f"assets/charsSprite/player/indigenaM/M6.png"), size),
                     pygame.transform.scale(pygame.image.load(f"assets/charsSprite/player/indigenaM/M7.png"), size)],
            "shot": [pygame.transform.scale(pygame.image.load(f"assets/charsSprite/player/indigenaM/S0.png"), size),
                     pygame.transform.scale(pygame.image.load(f"assets/charsSprite/player/indigenaM/S1.png"), size),
                     pygame.transform.scale(pygame.image.load(f"assets/charsSprite/player/indigenaM/S2.png"), size),
                     pygame.transform.scale(pygame.image.load(f"assets/charsSprite/player/indigenaM/S3.png"), size),
                     pygame.transform.scale(pygame.image.load(f"assets/charsSprite/player/indigenaM/S4.png"), size),
                     pygame.transform.scale(pygame.image.load(f"assets/charsSprite/player/indigenaM/S5.png"), size)],
            }    
                 
        # Definindo o estado inicial
        self.is_dead = False
        self.state = "idle"
        self.current_frame = 0  # Índice do quadro atual na lista de imagem
        self.image = self.animations[self.state][self.current_frame]  # Primeira Imagem
        self.rect = self.image.get_rect(topleft=position)  # Posição Inicial do jogador
        self.lives = 3  # Número de vidas (live)
        self.life = 25 #Pontos de Vida (Zerou os pontos perdeu uma Vida = Live)
        self.dialog_active = False  # Flag para indicar se o diálogo está ativo
        self.dialog_npc = None  # Referência ao NPC com o qual está dialogando
    
    def update(self):
        """Atualiza o estado do jogador em cada quadro."""
        super().update()  # Chama o método da classe pai sem argumentos
        self.gravity()  # Aplica a gravidade
        self.movements()  # Atualiza os movimentos laterais
        
        # Desabilita o movimento lateral se o personagem está no buraco
        if self.rect.y >= 486:
            self.right = False
            self.left = False
            
        # Lógica para movimento e atualização
        if self.is_dead:
            return  # Se o personagem está morto, não faz mais nada
        
        # Verifica se o jogador está no diálogo
        if self.dialog_active:
            return  # Se o diálogo estiver ativo, o jogador não pode se mover   

        if self.check_death():  # Chama a função check_death
            if self.lives <= 0:
                self.die()  # Chama o método de morte se as vidas acabaram
        # Lógica de movimento do jogador, animação, etc.    
    
    def start_dialogue(self, npc):
        """Inicia o diálogo com o NPC."""
        self.dialog_active = True
        npc.show_dialogue() # Exibe o diálogo do NPC

    def end_dialogue(self):
        """Encerra o diálogo."""
        self.dialog_active = False # Desativa o diálogo
    
    def gravity(self):
        """Aplica a gravidade ao jogador."""
        self.vel += self.grav  # Aumenta a velocidade de queda pela gravidade
        self.rect.y += self.vel  # Move o jogador para baixo

        # Limite a velocidade de queda
        if self.vel >= 10:
            self.vel = 10  # Limita a velocidade de queda

        # Verifica se o jogador está em uma área de buraco
        if 380 <= self.rect.x <= 480:
            self.check_death()  # Chama a função que "mata" o jogador ao cair no buraco
        else:
            # Caso contrário, verifica se o jogador atingiu o chão
            if self.rect.y >= GROUND_LEVEL - self.rect.height:  # Deve ser a altura do chão
                self.rect.y = GROUND_LEVEL - self.rect.height  # Reposiciona o jogador no chão
                self.vel = 0  # Reseta a velocidade ao tocar o chão
                self.on_ground = True  # Marca como estando no chão
            
    def events(self, events):
        """Processa eventos de teclado para controlar o jogador."""
        if events.type == pygame.KEYDOWN:
            if events.key == pygame.K_d or events.key == pygame.K_RIGHT:
                self.right = True
            elif events.key == pygame.K_a or events.key == pygame.K_LEFT:
                self.left = True
            elif events.key == pygame.K_SPACE and self.on_ground:  # Verifica se está no chão antes de pular
                self.vel = self.jump_power  # Faz o jogador pular
                self.on_ground = False  # Marca como não está mais no chão
                
            elif events.key == pygame.K_e:  # Tecla de ação para iniciar o diálogo
                if self.dialog_npc:  # Verifica se o jogador está perto de um NPC
                    self.start_dialogue(self.dialog_npc)
        
        elif events.type == pygame.KEYUP:
            if events.key == pygame.K_d or events.key == pygame.K_RIGHT:
                self.right = False
            elif events.key == pygame.K_a or events.key == pygame.K_LEFT:
                self.left = False
                
                
    def start_dialogue(self, npc):
        """Inicia o diálogo com o NPC."""
        self.dialog_active = True  # Ativa o diálogo
        print(f"{npc.__class__.__name__}: Bem-vindo, jovem guerreiro! O que procura?")
        # Aqui você pode adicionar mais lógicas para o diálogo, como exibir opções ou continuar com missões.
        # Durante o diálogo, o jogador não poderá se mover:
        self.is_moving = False  # Desativa o movimento do jogador

    def stop_dialogue(self):
        """Interrompe o diálogo."""
        self.dialog_active = False  # Desativa o diálogo
        self.is_moving = True  # Ativa novamente o movimento do jogador
        print("Diálogo finalizado.")            
    
    def movements(self):
        """Atualiza os movimentos laterais e a animação do jogador."""
        # Limite da tela (ajuste conforme o tamanho da tela)
        screen_width = 1280  # Largura da tela
        buffer = 75  # Permite ultrapassar 75px para fora dos limites da tela

        # Movimento para a direita
        if self.right:
            # Permite ultrapassar 75px além da borda direita
            if self.rect.x + self.rect.width - buffer < screen_width:
                self.rect.x += 2.8  # Move o jogador para a direita
            # Executa animação mesmo que esteja parado na borda
            self.animate("walk", 15, 7)  # Chama animação de caminhada para direita
            self.image = pygame.transform.flip(self.image, False, False)  # Imagem virada para a direita
            self.facing_right = True  # Atualiza a direção para a direita

        # Movimento para a esquerda
        elif self.left:
            # Permite ultrapassar 75px além da borda esquerda
            if self.rect.x + buffer > 0:
                self.rect.x -= 2.8  # Move o jogador para a esquerda
            # Executa animação mesmo que esteja parado na borda
            self.animate("walk", 15, 7)  # Chama animação de caminhada para esquerda
            self.image = pygame.transform.flip(self.image, True, False)  # Imagem virada para a esquerda
            self.facing_right = False  # Atualiza a direção para a esquerda

        # Caso contrário, animação de espera (idle)
        else:
            self.animate("idle", 100, 1)  # Animação de espera (idle)
            if self.facing_right:
                self.image = pygame.transform.flip(self.image, False, False)  # Mantém virado para a direita
            else:
                self.image = pygame.transform.flip(self.image, True, False)  # Mantém virado para a esquerda
    
    def animate(self, name, ticks, limit):
        """Anima o jogador com uma sequência de imagens."""
        self.ticks += 1  # Incrementa o contador de ticks

        # Controla a troca de frames com base no número de ticks
        if self.ticks >= ticks:
            self.ticks = 0  # Reseta o contador de ticks
            self.img += 1  # Avança para o próximo quadro da animação
            
        # Verifique o número de quadros disponíveis para a animação atual
        num_frames = len(self.animations[name])
        if self.img >= num_frames:  # Se chegou ao final dos quadros, reseta para o primeiro
            self.img = 0
            
        # Atualiza a imagem do jogador com a nova animação
        self.image = pygame.transform.scale(self.animations[name][self.img], self.size)
    
    def check_death(self):
        """Verifica se o jogador caiu fora da tela e reposiciona se necessário."""
        if self.rect.y > BASE_HEIGHT:
            self.lives -= 1  # Perde uma vida
            if self.lives > 0:
                self.rect.x, self.rect.y = 100, 250  # Reposiciona o jogador após a queda
                return True
            else:
                # Ação quando as vidas acabam, como mostrar uma tela de Game Over
                return False
        
        # Outras condições de morte podem ser verificadas aqui
        # Por exemplo, colisões com inimigos, limites de tempo, etc.
        
        return False
    
    def lose_life(self):
        """Chama a função para perder uma vida."""
        self.lives -= 1  # Diminui a quantidade de vidas
        if self.lives <= 0:
            self.die()  # Se não tiver mais vidas, chama a função de morte
    
    def die(self):
        """Define o estado do personagem como morto."""
        self.is_dead = True

         
class NPC_Cacique(Obj):
    """Classe para representar o NPC estático 'Cacique' com animação idle sempre virado para a esquerda."""

    def __init__(self, image_path, position, groups, size=(200, 200)):
        super().__init__(image_path, position, groups, size)  # Adiciona o NPC ao grupo de sprites
        self.size = size
        self.original_image = pygame.image.load("assets/charsSprite/npcs/Cacique/CR0.png").convert_alpha()
        self.original_image = pygame.transform.flip(self.original_image, True, False)  # Inverte a imagem para a esquerda
        self.image = pygame.transform.scale(self.original_image, size)  # Redimensiona para 200x200
        self.rect = self.image.get_rect(topleft=position)  # Define a posição inicial do NPC
    
        # Inicializa o dicionário de animações
        self.animations = {
            "idle": []  # Inicializando a chave 'idle' com uma lista vazia
        }

        # Carregar imagens da animação idle
        for i in range(2):  # Assumindo que você tem 2 imagens para a animação idle
            img = pygame.image.load(f"assets/charsSprite/npcs/Cacique/CR{i}.png").convert_alpha()
            img = pygame.transform.flip(img, True, False)  # Inverte as imagens para a esquerda
            img = pygame.transform.scale(img, size)  # Redimensiona
            self.animations["idle"].append(img)  # Adiciona à lista de animação

        self.state = "idle"  # Estado inicial
        self.current_frame = 0  # Índice do quadro atual na lista de imagem
        self.image = self.animations[self.state][self.current_frame]  # Primeira imagem da animação
        self.rect = self.image.get_rect(topleft=position)  # Atualiza a posição do NPC
        
        # Inicializando o contador de ticks para animação
        self.ticks = 0  # Certifique-se de inicializar os ticks aqui!
        self.img = 0  # Índice da imagem atual para animação

    def update(self):
        """Atualiza o estado do NPC em cada quadro."""
        self.animate("idle", 100, 1)  # Atualiza a animação de respiração (idle)

    def animate(self, name, ticks, limit):
        """Anima o NPC com uma sequência de imagens."""
        self.ticks += 1  # Incrementa o contador de ticks

        # Controla a troca de frames com base no número de ticks
        if self.ticks >= ticks:
            self.ticks = 0  # Reseta o contador de ticks
            self.current_frame += 1  # Avança para o próximo quadro da animação

        # Verifica se a animação chegou ao fim e reseta o contador
        num_frames = len(self.animations[name])
        if self.current_frame >= num_frames:  # Porque temos apenas 2 imagens (0 e 1)
            self.current_frame = 0  # Reseta para a primeira imagem da animação

        # Atualiza a imagem do NPC com a nova animação
        self.image = pygame.transform.scale(self.animations[name][self.current_frame], self.size)

    def interact(self, player):
        """Interage com o jogador quando um evento específico ocorre."""
        # Exemplo de interação: quando o jogador está perto do Cacique
        if self.rect.colliderect(player.rect):  # Verifica se o jogador está próximo
            print("Cacique: Bem-vindo, jovem guerreiro. O que procura?")
            # Aqui, você pode disparar um evento específico ou diálogo
            # Exemplo: abrir um menu ou dar uma missão
            

class ChatBox:
    """Classe para exibir mensagens de diálogo na tela."""

    def __init__(self, font, position, size):
        self.font = font  # Fonte padrão para diálogos
        self.small_font = pygame.font.Font(None, 24)  # Fonte menor para perguntas e alternativas
        self.position = position
        self.size = size
        self.rect = pygame.Rect(position, size)
        self.color = (BLACK_COLOR)
        self.text_color = (WHITE_COLOR)
        self.messages = []  # Lista de mensagens/questões
        self.current_message = 0  # Índice da mensagem atual
        self.active = False  # Indica se o chatbox está ativo
        self.option_index = 0  # Índice da opção selecionada
        self.score = 0  # Pontuação do jogador
        self.title = ""  # Título da pergunta
        self.question = ""  # Texto da pergunta
        self.options = []  # Opções de resposta
        self.correct_answers = []  # Respostas corretas das questões

    def display_messages(self, messages):
        """Ativa o chatbox com um conjunto de mensagens."""
        # Converte as mensagens para strings, se necessário
        self.messages = [str(msg) for msg in messages]
        self.current_message = 0
        self.active = True
        self.options = []  # Limpa opções de resposta

    def display_question(self, title, question, options):
        """Exibe uma pergunta com título e opções."""
        self.title = title  # Define o título da pergunta
        self.question = question if isinstance(question, str) else ' '.join(question)  # Garante que a pergunta seja string
        self.options = options  # Define as opções de resposta
        self.option_index = 0  # Reseta o índice da opção selecionada
        self.active = True  # Ativa o chatbox para exibição

    def next_message(self):
        """Avança para a próxima mensagem ou termina o diálogo."""
        if self.options:  # Se houver opções, não avança mais mensagens
            return
        self.current_message += 1
        if self.current_message >= len(self.messages):  # Termina o diálogo
            self.active = False  # Desativa o chatbox

    def validate_answer(self):
        """Valida a resposta do jogador e avança o diálogo."""
        if self.options and self.correct_answers:
            selected_option = self.options[self.option_index]
            if selected_option == self.correct_answers[0]:  # Verifica se está correto
                self.score += 1
                print("Resposta correta!")
            else:
                print("Resposta errada.")
            self.active = False  # Fecha a questão

    def previous_option(self):
        """Move para a opção anterior."""
        if self.options:
            self.option_index = (self.option_index - 1) % len(self.options)

    def next_option(self):
        """Move para a próxima opção."""
        if self.options:
            self.option_index = (self.option_index + 1) % len(self.options)
            
    def select_option(self):
        """Retorna a opção atualmente selecionada."""
        if self.options:  # Certifica-se de que há opções disponíveis
            return self.options[self.option_index]
        return None  # Caso não haja opções, retorna None        

    def is_active(self):
        """Verifica se o chatbox está ativo."""
        return self.active

    def draw(self, screen):
        """Desenha a chatbox e seu conteúdo na tela."""
        if not self.active:
            return  # Não desenha nada se o chatbox não estiver ativo

        # Desenhar o retângulo do chatbox
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

        # Define a margem e calcula o espaço disponível
        margin = 20  # Margem de 20px em torno do texto
        available_height = self.rect.height - 2 * margin
        y_offset = self.rect.y + margin

        # Exibir título, se houver, e atualizar o espaço disponível
        if self.title:
            title_surface = self.font.render(self.title, True, self.text_color)
            screen.blit(title_surface, (self.rect.x + margin, y_offset))
            y_offset += 40  # Espaço após o título
            available_height -= 40

        # Exibir pergunta, se houver
        if self.question:
            wrapped_question = self.wrap_text(str(self.question), self.rect.width - 2 * margin)
            for line in wrapped_question:
                if available_height < 20:  # Verifica se há espaço para desenhar
                    break
                question_surface = self.font.render(line, True, self.text_color)
                screen.blit(question_surface, (self.rect.x + margin, y_offset))
                y_offset += 20  # Espaço entre as linhas da pergunta
                available_height -= 20

        # Exibir opções, se houver
        if self.options:
            y_offset += 20  # Espaço entre a pergunta e as opções
            available_height -= 20
            for i, option in enumerate(self.options):
                wrapped_option = self.wrap_text(str(option), self.rect.width - 2 * margin, self.small_font)
                for line in wrapped_option:
                    if available_height < 20:  # Verifica se há espaço para desenhar
                        break
                    color = (255, 255, 0) if i == self.option_index else self.text_color  # Amarelo para a opção selecionada
                    option_surface = self.small_font.render(line, True, color)
                    screen.blit(option_surface, (self.rect.x + margin, y_offset))
                    y_offset += 20  # Espaço entre as linhas da opção
                    available_height -= 20
                y_offset += 10  # Espaço extra entre as opções

        # Exibir mensagem atual (para diálogos simples)
        elif self.messages and self.current_message < len(self.messages):
            wrapped_message = self.wrap_text(self.messages[self.current_message], self.rect.width - 2 * margin)
            for line in wrapped_message:
                if available_height < 30:  # Verifica se há espaço para desenhar
                    break
                message_surface = self.font.render(line, True, self.text_color)
                screen.blit(message_surface, (self.rect.x + margin, y_offset))
                y_offset += 30  # Espaço entre as linhas
                available_height -= 30
                
    def wrap_text(self, text, max_width, font=None):
        """Divide o texto em múltiplas linhas para caber na largura da caixa."""
        if text is None:
            return []  # Retorna uma lista vazia se o texto for None
        if font is None:
            font = self.font  # Usa a fonte padrão se nenhuma for especificada
        words = text.split(' ')  # Garante que `text` seja uma string
        lines = []
        current_line = []

        for word in words:
            current_line.append(word)
            test_line = ' '.join(current_line)
            if font.size(test_line)[0] > max_width:
                current_line.pop()  # Remove a última palavra que excedeu
                lines.append(' '.join(current_line))
                current_line = [word]

        if current_line:  # Adiciona a última linha
            lines.append(' '.join(current_line))

        return lines
                
# Biblioteca de diálogos
class Dialogo:
    """Biblioteca contendo os diálogos da interação entre o jogador e o NPC."""
    falas = [
        ("Cacique:",
            "Jovem guerreiro, o momento é grave! O equilíbrio sagrado que protege nossa terra foi rompido!!!"),
        ("Jovem Guerreiro:",
            "Como isso poderia acontecer? O Ídolo guardava o espírito das nossas florestas e rios..."),
        ("Cacique:",
            "Forças sombrias o usurparam, e agora o equilíbrio natural se desfaz! As criaturas místicas, que antes viviam em harmonia conosco, tornaram-se ferozes e hostis! Seus ataques ameaçaram nossa terra e até os guardiões ancestrais!"),
        ("Jovem Guerreiro:",
            "...precisamos recuperá-lo! Mas como enfrentar tamanha ameaça?"),            
        ("Cacique:",
            "Para isso, você deve provar que carrega a sabedoria dos nossos ancestrais! Somente aquele que compreende as tradições estará pronto para a missão! Passe por estes cinco testes, e verá que está preparado para seguir nesta jornada!!!"),
        ("Cacique:",
            "Agora você está pronto para entender: 'ESTA JORNADA NÃO É APENAS SUA'!!! Guerreiros de todas as culturas devem unir suas forças! Cada povo carrega saberes únicos que serão essenciais nesta missão! Juntos, restauraremos o sagrado em seu local de origem!!!"),
        ("Jovem Guerreiro:",
            "Seremos a voz dos antigos e a força dos Deuses! Recuperaremos o Ídolo e traremos a paz de volta!"),
        ("Cacique:",
            "Lembre-se, a força verdadeira reside não nos braços, mas na união dos corações e na sabedoria compartilhada! Vá, encontre outros guerreiros, e juntos, tragam de volta a paz para nossa terra!!!"), 
    ]

# Biblioteca de questões
class Questoes:
    """Biblioteca contendo as questões e respostas do teste de conhecimento."""
    perguntas = [
        {
            "titulo": "Questão: O Som da Natureza:",
            "pergunta": "Nossa música é mais do que som: é uma oração viva, conectando-nos aos espíritos das matas e rios. Diga-me, jovem guerreiro, quais instrumentos nossos ancestrais utilizam para conversar com os deuses da natureza?",
            "opcoes": [
                "Instrumentos de sopro, moldados com bambu ou ossos, que imitam o vento e os animais.",
                "Instrumentos de percussão, feitos com troncos ocos e couro animal, que ressoam como o coração da terra.",
                "Instrumentos de corda, esculpidos com habilidade, ressoando melodias da alma humana.",
                "Instrumentos eletrônicos, que dependem da energia dos homens, não da natureza."
            ],
            "resposta_correta": "Instrumentos de sopro, moldados com bambu ou ossos, que imitam o vento e os animais.",
        },
        {
            "titulo": "Questão: A Arte da Luta:",
            "pergunta": "A verdadeira força vem do espírito e da tradição. Qual luta ancestral herdamos, usada não só para defender, mas para honrar nossa cultura?",
            "opcoes": [
                "Jiu-jitsu, técnica de domínio pelo chão, mas de origem distante.",
                "Huka-Huka, combate de levantamentos e derrubadas.",
                "Capoeira, luta-dança de outras influências culturais.",
                "Boxe, a arte dos punhos, que veio de terras estrangeiras.",
            ],
            "resposta_correta": "Huka-Huka, combate de levantamentos e derrubadas."
        },
        {
            "titulo": "Questão: Escrita Ancestral:",
            "pergunta": "Antes da chegada de outros povos, nossos ancestrais já narraram histórias com símbolos vivos. Que forma de comunicação usamos para registrar saberes e tradições?",
            "opcoes": [
                "Faixas Decorativas com formas geométricas, linhas e tramas em estamparia de roupas, em que as cores também são classificadas como um sistema de código e escrita de acordo com a comunidade a que está vinculada.",
                "Caligrafia, uso de tintas e papiros para registro de palavras, usanto elementos simbólicos ou signos, que representam letras e números.",
                "Pedras com símbolos esculpidos que são conhecidas como 'Runas', sendo jogadas e dependendo da ordem e sequencia que caírem significa uma informação.",
                "Pinturas Corporais, com achuras, linhas e tramas, que utilizam pigmentos naturais extraídos de minérios e vegetais, representando o nível de responsabilidade e importancia da pessoa dentro da comunidade que atua."
            ],
            "resposta_correta": "Pinturas Corporais, com achuras, linhas e tramas, que utilizam pigmentos naturais extraídos de minérios e vegetais, representando o nível de responsabilidade e importancia da pessoa dentro da comunidade que atua."
        },
        {
            "titulo": "Questão: Palavras do Espírito Ancestral",
            "pergunta": "Nossa língua vive em palavras que muitos falam sem conhecer sua origem. Quais são as origens do coração da nossa terra?",
            "opcoes": [
                "Mesa, Relógio, Camiseta, Hospital, Cerveja.",
                "Zen, Quimono, Origami, Chá, Sushi.",
                "Igarapé, Jabuticaba, Caiçara, Mirim, Pindorama.",
                "Moleque, Maracatu, Caxixi, Fubá, Dendê."
            ],
            "resposta_correta": "Igarapé, Jabuticaba, Caiçara, Mirim, Pindorama."
        },
        {
            "titulo": "Questão: O Alimento da Terra:",
            "pergunta": "A terra nos sustenta e a comida que cultivamos reflete quem somos. Qual é a essência da nossa culinária, que fortalece o corpo e honra a tradição?",
            "opcoes": [
                "Mandioca, Milho, Peixe, Frutas, Carne.",
                "Milho, Feijão, Mandioca, Dendê, Couve.",
                "Peixe, Batata, Trigo, Azeite, Ervas.",
                "Peixe, Arroz, Algas, Shoyu, Tofu."
            ],
            "resposta_correta": "Mandioca, Milho, Peixe, Frutas, Carne."
        },
    ]
            
