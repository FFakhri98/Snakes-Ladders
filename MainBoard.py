import pygame

pygame.init()

#تنظیمات صفحه اصلی
width=800
height=800
CellSize=width//10

#رنگ ها
white=(255, 255, 255)
black=(0, 0, 0)
yellow=(247, 246, 178)
red=(247, 178, 178)

#صفحه و فونت
board=pygame.display.set_mode((width,height))
cap=pygame.display.set_caption("snakes and ladders")
font=pygame.font.SysFont("arial",12)


def draw_board():
    for row in range(10):
        for col in range(10):
            if row %2==0:
                RealCol=col
            else:
                RealCol=9-col
            #شماره خانه
            CellNum=row*10+RealCol+1  
        
            
            #مختصات هر خانه
            x=col*CellSize
            y=row*CellSize

            

            if (row+col)%2==0:
                color=yellow
            else:
                color=red
            #xو y گوشه سمت چپ خونه 
            #cellsize طول و ارتفاع
            pygame.draw.rect(board,color,(x,y,CellSize,CellSize)) 
            pygame.draw.rect(board,white,(x,y,CellSize,CellSize),2) 


            #رسم شماره خانه ها
            #اول عدد رو استرینگ میکنیم بعد تبدیل به عکس میکنیم بعد میچسبونیم
            board.blit( font.render(str(CellNum),True,black)  , (x + 7, y + 7)) 







running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    board.fill(white)
    draw_board()
    pygame.display.flip()

pygame.quit()
 



