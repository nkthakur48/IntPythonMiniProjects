# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2

VEL_OFFSET = 5


# helper function that spawns a ball by updating the 
# ball's position vector and velocity vector
# if right is True, the ball's velocity is upper right, else upper left
def ball_init(right):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH/2,HEIGHT/2]
    if right == True:
        ball_vel = [random.randrange(120, 240)/60,
                    -1 * random.randrange(60, 180)/60]
    elif right == False:
        ball_vel = [-1 * random.randrange(120, 240)/60,
                    -1 * random.randrange(60, 180)/60]

# define event handlers

def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are floats
    global score1, score2  # these are ints
    
    paddle1_pos = HEIGHT / 2
    paddle2_pos = HEIGHT / 2
    
    paddle1_vel = 0
    paddle2_vel = 0
    
    score1 = 0
    score2 = 0
    
    ball_init(random.choice((True,False)))

def draw(c):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
 
    # update paddle's vertical position, keep paddle on the screen
    if(paddle1_pos + paddle1_vel) >= HALF_PAD_HEIGHT and (paddle1_pos + paddle1_vel) <= (HEIGHT-HALF_PAD_HEIGHT):
        paddle1_pos += paddle1_vel
        
    if(paddle2_pos + paddle2_vel) >= HALF_PAD_HEIGHT and (paddle2_pos + paddle2_vel) <= (HEIGHT-HALF_PAD_HEIGHT):
        paddle2_pos += paddle2_vel
    
    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    
    # draw paddles
    #draw paddle1
    c.draw_polygon([(0,paddle1_pos - HALF_PAD_HEIGHT), (0, paddle1_pos + HALF_PAD_HEIGHT)
                    ,(PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT),(PAD_WIDTH,paddle1_pos - HALF_PAD_HEIGHT)]
                    ,1, "White", "White")
    
    #draw paddle2
    c.draw_polygon([(WIDTH-PAD_WIDTH,paddle2_pos - HALF_PAD_HEIGHT), (WIDTH-PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT)
                    ,(WIDTH, paddle2_pos + HALF_PAD_HEIGHT),(WIDTH,paddle2_pos - HALF_PAD_HEIGHT)]
                    ,1, "White", "White")
    
    # collide and reflect off of top side of canvas    
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    
    # collide and reflect off of bottom side of canvas    
    if ball_pos[1] >= (HEIGHT-1)-BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    
    # call ball_init(opp)when ball touches left gutter
    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:
        if (paddle1_pos - HALF_PAD_HEIGHT) <= ball_pos[1] <= (paddle1_pos + HALF_PAD_HEIGHT):
            ball_vel[0] *= -1.1
            ball_vel[1] *= 1.1
        else:
            score2 += 1
            ball_init(True)
        
    # call ball_init(opp)when ball touches right gutter    
    if ball_pos[0] >= (WIDTH-1)-BALL_RADIUS - PAD_WIDTH:
        if (paddle2_pos - HALF_PAD_HEIGHT) <= ball_pos[1] <= (paddle2_pos + HALF_PAD_HEIGHT):
            ball_vel[0] *= -1.1
            ball_vel[1] *= 1.1
        else:
            score1 += 1
            ball_init(False)

    
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # draw ball and scores
    c.draw_circle(ball_pos, 20, 1, "Red", "White")
    c.draw_text(str(score1),(WIDTH/4,HEIGHT/4), 36, "White")
    c.draw_text(str(score2),(WIDTH*3/4,HEIGHT/4), 36, "White")
    
def keydown(key):
    global paddle1_vel, paddle2_vel
    
      
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel -= VEL_OFFSET
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel += VEL_OFFSET
        
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel -= VEL_OFFSET
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel += VEL_OFFSET
        

   
def keyup(key):
    global paddle1_vel, paddle2_vel
    
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
        
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0

def reset_button_handler():
    new_game()


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
reset_button = frame.add_button("Reset Game", reset_button_handler)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)



# start frame
frame.start()

#start the game
new_game()
