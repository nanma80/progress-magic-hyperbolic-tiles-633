#!/usr/bin/env python

import os
import sys
import time
import datetime

filename_init = 'solved.log'
filename_current = 'solving.log'

if len(sys.argv) == 2:
  filename, filename_current = sys.argv

n_stickers_per_cell = 1 + 9 + 27 + 18 # total = 55
n_cells = 12
n_characters_per_sticker = 1
line_number_timer = 5

# print the clean and dirty indices
debug_mode = False

# the following is wrong
index_cell = [54] # 1
index_face = [0, 36, 6, 42, 12, 48, 18, 24, 30] # 9
index_edge = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53] # 27
index_vertex = [2, 4, 8, 10, 14, 16, 20, 22, 26, 28, 32, 34, 38, 40, 44, 46, 50, 52] # 18

index_types = [
  {'name': 'Cells', 'ind': index_cell, 'nColor':1},
  {'name': 'Faces', 'ind': index_face, 'nColor':2},
  {'name': 'Edges', 'ind': index_edge, 'nColor':3},
  {'name': 'Verti', 'ind': index_vertex, 'nColor':4}]

def read_status(filename):
  file = open(filename,'r')
  counter = 0
  status_code = ''
  for line in file:
    counter += 1
    if counter <= 1:
      continue
    status_code += line[:-1]
    if counter >= line_number_timer - 1:
      break

  for line in file:
    timemille = line[6:]
    timedt = datetime.timedelta(milliseconds = eval(timemille))
    break
  
  file.close()
  
  status_for_cell = [status_code[i_cell * n_stickers_per_cell * n_characters_per_sticker : (i_cell+1) * n_stickers_per_cell * n_characters_per_sticker] for i_cell in range(n_cells)]
  status = [ [ entry[i:i+n_characters_per_sticker] for i in range(0, len(entry), n_characters_per_sticker)   ]        for entry in status_for_cell ]
  return (timedt, status)

def compare_status():
  print('Current time:', datetime.datetime.now())
  (initTime, initStatus) = read_status (filename_init)  
  (curTime, curStatus) = read_status (filename_current)

  progressVector = []
  for i in range(0, n_stickers_per_cell):
    progressVector.append(0)

  incomplete_indices = set()
  
  completedType = {}
  for type in index_types:
    completedType[type['name']] = 0
  
  for i in range(0,n_cells):
    for j in range(0,n_stickers_per_cell):
      if initStatus[i][j] == curStatus[i][j]:
        progressVector[j] += 1
      else:
        incomplete_indices.add(j)

    for type in index_types:
      flag = True
      for j in type['ind']:
        if initStatus[i][j] != curStatus[i][j]:
          flag = False
          break
      if flag:
        completedType [type['name']] += 1

  if debug_mode:
    print('Dirty indices:')
    print(sorted(list(incomplete_indices)))
    print(len(incomplete_indices))
    print('Clean indices:')
    clean_indices = set(range(n_stickers_per_cell)) - incomplete_indices
    print(sorted(list( clean_indices )))
    print(len(clean_indices))

  print('----------------------------------------------------------------------------')
  print('Type \tSolved Pieces\tSolved Stickers\tPercentage\tCompleted Cells')
  print('----------------------------------------------------------------------------')
  
  for type in index_types:
    totalSolvedSticker = sum([progressVector[i] for i in type['ind']])
    totalSticker = n_cells * len(type['ind'])
    totalSolvedPiece = totalSolvedSticker/type['nColor']
    totalPiece = totalSticker/type['nColor']
    
    percentage = 100.0 * totalSolvedPiece / totalPiece
    
    print(type['name']+': \t%4d/%4d, \t%4d/%4d, \t%6.2f'%(totalSolvedPiece, totalPiece, totalSolvedSticker,totalSticker,percentage)+'%, '+('\t%3d/%3d'%(completedType[type['name']],n_cells)))
    
  print('----------------------------------------------------------------------------')
  hours = curTime.seconds/3600
  totalhours = curTime.days * 24 + hours
  minutes = (curTime.seconds%3600)/60
  minutesStr = str(100 + minutes)[1:]
  seconds = curTime.seconds%60
  secondsStr = str(100 + seconds)[1:]
  milliseconds = curTime.microseconds/1000
  millisecondsStr = str(1000 + milliseconds)[1:]
  print ('Current solving time is: %s'%(str(curTime)[:-3]))

def main():
  last_update_time = -1

  while True:
    new_update_time = os.stat(filename_current).st_mtime
    if new_update_time - last_update_time > 1:
      print('File updated, analyze status')  
      compare_status()
      last_update_time = new_update_time
      print('Press Ctrl-C to exit')
    time.sleep(5)

if __name__ == '__main__':
  main()
