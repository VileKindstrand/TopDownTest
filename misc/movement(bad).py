
class dipshit: 
    def movement(self):

        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            for sprite in self.game.all_sprites:
                sprite.rect.x += PLAYER_SPEED
            self.x_change  -= PLAYER_SPEED
            self.facing = 'left'
        if keys[pygame.K_RIGHT]:
            for sprite in self.game.all_sprites:
                sprite.rect.x -= PLAYER_SPEED
            self.x_change += PLAYER_SPEED
            self.facing = 'right'
        if keys[pygame.K_UP]:
            for sprite in self.game.all_sprites:
                sprite.rect.y += PLAYER_SPEED
            self.y_change -= PLAYER_SPEED
            #self.facing = 'up'
        if keys[pygame.K_DOWN]:
            for sprite in self.game.all_sprites:
                sprite.rect.y -= PLAYER_SPEED
            self.y_change += PLAYER_SPEED
            #self.facing = 'down'
        
        
        if keys[pygame.K_DOWN] and keys[pygame.K_LEFT]:
            pass
        elif keys[pygame.K_DOWN]:
            pass
        elif keys[pygame.K_LEFT]:
            pass

        if keys[pygame.K_DOWN] and keys[pygame.K_RIGHT]:
            pass
        elif keys[pygame.K_DOWN]:
            pass
        elif keys[pygame.K_RIGHT]:
            pass

        if keys[pygame.K_UP] and keys[pygame.K_LEFT]:
            pass
        elif keys[pygame.K_UP]:
            pass
        elif keys[pygame.K_LEFT]:
            pass

        if keys[pygame.K_UP] and keys[pygame.K_RIGHT]:
            pass
        elif keys[pygame.K_UP]:
            pass
        elif keys[pygame.K_RIGHT]:
            pass