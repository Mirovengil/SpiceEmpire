'''
В этом модуле реализовано приобретение новых кораблей, а именно:
> Отслеживание и изменение количества лимитов у каждого игрока;
> Обмен лимитов игрока на корабли;
'''

from random import randint
import class_planet

#Лимиты игрокам будут выдаваться с вероятностью 1/POSSIBILITY каждый ход.

def add_limits(game_map, possibility=3):
    '''
    С некоторой вероятностью начислит игроку лимиты за каждую его планету.
    Вероятность для каждой планеты вычисляется отдельно, чтобы "всё сильнее, сильнее
    накал".
    '''
    if randint(0, 100) % possibility != 0:
        return 0
    game_map.limits = [0 for i in range(game_map.number_of_players)]
    star = 0
    while star < len(game_map.stars):
        planet = 0
        while planet < len(game_map.stars[star].planets):
            if game_map.stars[star].planets[planet].master != -1:
                game_map.limits[game_map.stars[star].planets[planet].master] +=\
                game_map.stars[star].planets[planet].limits[class_planet.Planet.LIM_SIZE]
            planet += 1
        star += 1
    ship = 0
    while ship < len(game_map.ships):
        game_map.limits[game_map.ships[ship].master] -= game_map.ships[ship].limit
        ship += 1
