import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Paint App")
    clock = pygame.time.Clock()

    
    canvas = pygame.Surface(screen.get_size())
    canvas.fill((0, 0, 0))

    radius = 15                  
    mode = 'blue'                
    drawing = False             
    tool = 'brush'              
    start_pos = None          

    while True:
        pressed = pygame.key.get_pressed()
        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]

        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and ctrl_held:
                    return
                if event.key == pygame.K_F4 and alt_held:
                    return
                if event.key == pygame.K_ESCAPE:
                    return
                
                if event.key == pygame.K_r:
                    mode = 'red'
                elif event.key == pygame.K_g:
                    mode = 'green'
                elif event.key == pygame.K_b:
                    mode = 'blue'
                
                elif event.key == pygame.K_e:
                    tool = 'eraser'
                elif event.key == pygame.K_c:
                    tool = 'circle'
                elif event.key == pygame.K_s:
                    tool = 'rectangle'
                elif event.key == pygame.K_p:
                    tool = 'brush'
            
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  
                    drawing = True
                    start_pos = event.pos 
                  
                    if tool in ['brush', 'eraser']:
                        color = (0, 0, 0) if tool == 'eraser' else get_color(mode)
                        pygame.draw.circle(canvas, color, event.pos, radius)
                elif event.button == 4:  
                    radius = min(200, radius + 1)
                elif event.button == 5: 
                    radius = max(1, radius - 1)
            
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drawing = False 
                    end_pos = event.pos  
                    
                    if tool == 'rectangle':
                        rect = pygame.Rect(start_pos, (end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]))
                        pygame.draw.rect(canvas, get_color(mode), rect, 2)
                    elif tool == 'circle':
                        rect = pygame.Rect(start_pos, (end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]))
                        pygame.draw.ellipse(canvas, get_color(mode), rect, 2)
            
            if event.type == pygame.MOUSEMOTION:
               
                if drawing and tool in ['brush', 'eraser']:
                    color = (0, 0, 0) if tool == 'eraser' else get_color(mode)
                    pygame.draw.circle(canvas, color, event.pos, radius)

        
        screen.blit(canvas, (0, 0))
        pygame.display.flip()
        clock.tick(60)

def get_color(color_mode):
   
    colors = {
        'blue': (0, 0, 255),
        'red': (255, 0, 0),
        'green': (0, 255, 0)
    }
    return colors.get(color_mode, (255, 255, 255))

main()
