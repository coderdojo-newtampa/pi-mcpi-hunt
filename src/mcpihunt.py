#
# mcpihunt game
#

import mcpi.minecraft as minecraft
import mcpi.block as block
import mcpi.vec3 as vec3
import math as math
import time as time
import random

mc = minecraft.Minecraft.create()
gems = []
compass_height = 4
old_compass_pos = vec3.Vec3(0,compass_height,0)

#
# Creates a new gem in the world
#
# This function creates a new gem by:
#   * Finding an empty random position in the world
#   * Storing the coordinate as a Vec3 object in the gems list
#   * Creating a block for the gem
#   * Function returns gem location as Vec3
#
def create_gem(radius):
    while True:
        x=random.randrange(-radius,radius)
        z=random.randrange(-radius,radius)
        y = mc.getHeight(x,z)

        block_beneath = mc.getBlock(x, y - 1, z)
        if (block_beneath not in {block.AIR.id, block.WATER.id, block.WATER_STATIONARY.id, block.WATER_FLOWING.id}):
        #        mc.player.setPos(x,y,z)
        #        mc.postToChat("Teleported!")
            done = True
        gem = vec3.Vec3(x,y,z)
        gems.append(gem)
        mc.setBlock(gem.x, gem.y, gem.z, block.GLOWING_OBSIDIAN.id)
        return gem

def closest_gem(p1):
    shortest_dist=9999999
    shortest_index=-1

    for index, p0 in enumerate(gems):
        xdiff = p0.x - p1.x
        zdiff = p0.z - p1.z

        dist = math.hypot(xdiff, zdiff)
        if (dist <= shortest_dist):
            shortest_dist = dist
            shortest_index = index

    if (shortest_dist < 9999999):
        return gems[shortest_index]
    else:
        return None

def show_compass(pos):
    blocks = []

    blocks.append(mc.getBlock(pos.x + 5, pos.y + compass_height, pos.z))
    blocks.append(mc.getBlock(pos.x - 5, pos.y + compass_height, pos.z))
    blocks.append(mc.getBlock(pos.x, pos.y + compass_height, pos.z + 5))
    blocks.append(mc.getBlock(pos.x, pos.y + compass_height, pos.z - 5))

    mc.setBlock(pos.x + 5, pos.y + compass_height, pos.z, block.WOOL.id, 1)
    mc.setBlock(pos.x - 5, pos.y + compass_height, pos.z, block.WOOL.id, 2)
    mc.setBlock(pos.x, pos.y + compass_height, pos.z + 5, block.WOOL.id, 3)
    mc.setBlock(pos.x, pos.y + compass_height, pos.z - 5, block.WOOL.id, 4)

    time.sleep(1)

    mc.setBlock(pos.x + 5, pos.y + compass_height, pos.z, blocks[0])
    mc.setBlock(pos.x - 5, pos.y + compass_height, pos.z, blocks[1])
    mc.setBlock(pos.x, pos.y + compass_height, pos.z + 5, blocks[2])
    mc.setBlock(pos.x, pos.y + compass_height, pos.z - 5, blocks[3])

def compass(pos, gem):
    p0 = pos
    p1 = gem

    xdiff = p1.x - p0.x
    zdiff = p1.z - p0.z

    if (xdiff > 0):
        print("East ", xdiff)
    else:
        print("West ", xdiff)

    if (zdiff > 0):
        print("South ", zdiff)
    else:
        print("North ", zdiff)

def check_blocks(pos):

    for index, gem in enumerate(gems):
        if ((pos.x > gem.x - 2 and pos.x < gem.x + 2) and
            (pos.y > gem.y - 2 and pos.y < gem.y + 2) and
                (pos.z > gem.z - 2 and pos.z < gem.z + 2)):

                print("Block found at index ", index)
                print("Gems size ", len(gems))
                gems.pop(index)
                mc.setBlock(gem.x, gem.y, gem.z, block.AIR.id)

# Number of gems for player to find
for i in range(2):

    # The number we pass is the "radius" how far away to place gems, bigger number means more difficulty
    # Don't exceed around 150
    gem = create_gem(5)

while True:
    print(gems)
    pos = mc.player.getPos()
    gem = closest_gem(pos)
    print(gem)

    if gem:
       compass(pos, gem)
    show_compass(pos)
    check_blocks(pos)
    time.sleep(0.5)