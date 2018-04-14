beatTime = 100/60
bassOn = 1
A = :A
B = :B
C = :C
D = :D
E = :E
F = :F
G = :G
aa1,bb1,cc1,dd1,ee1,ff1,gg1 =  ""
aa2,bb2,cc2,dd2,ee2,ff2,gg2 =  ""
aa3,bb3,cc3,dd3,ee3,ff3,gg3 =  ""
aa4,bb4,cc4,dd4,ee4,ff4,gg4 =  ""

aamp = 0
bamp = 0
camp = 0
damp = 0
eamp = 0
famp = 0
gamp = 0

live_loop :GetNotesFromOSC do
  use_real_time
  track, useBass, a, b, c, d, e, f, g, h = sync "/osc/trigger/prophet"
  bassOn = useBass
  
  if(track == 0)
    aa1,bb1,cc1,dd1,ee1,ff1,gg1 =  ""
    aa2,bb2,cc2,dd2,ee2,ff2,gg2 =  ""
    aa3,bb3,cc3,dd3,ee3,ff3,gg3 =  ""
    aa4,bb4,cc4,dd4,ee4,ff4,gg4 =  ""
  end
  
  if(track == 1)
    aa1 = a
    bb1 = b
    cc1 = c
    dd1 = d
    ee1 = e
    ff1 = f
    gg1 = g
  end
  if(track == 2)
    aa2 = a
    bb2 = b
    cc2 = c
    dd2 = d
    ee2 = e
    ff2 = f
    gg2 = g
  end
  if(track == 3)
    aa3 = a
    bb3 = b
    cc3 = c
    dd3 = d
    ee3 = e
    ff3 = f
    gg3 = g
  end
  if(track == 4)
    aa4 = a
    bb4 = b
    cc4 = c
    dd4 = d
    ee4 = e
    ff4 = f
    gg4 = g
  end
  
end

live_loop :bass do
  use_real_time
  if(bassOn = 1)
    sample :bd_haus
  end
  
  sleep beatTime
end

live_loop :ChordPlayOne do
  findAndPlayTone aa1
  findAndPlayTone bb1
  findAndPlayTone cc1
  findAndPlayTone dd1
  findAndPlayTone ee1
  findAndPlayTone ff1
  findAndPlayTone gg1
end

live_loop :ChordPlayTwo do
  findAndPlayTone aa2
  findAndPlayTone bb2
  findAndPlayTone cc2
  findAndPlayTone dd2
  findAndPlayTone ee2
  findAndPlayTone ff2
  findAndPlayTone gg2
end

live_loop :ChordPlayThree do
  findAndPlayTone aa3
  findAndPlayTone bb3
  findAndPlayTone cc3
  findAndPlayTone dd3
  findAndPlayTone ee3
  findAndPlayTone ff3
  findAndPlayTone gg3
end

live_loop :ChordPlayThree do
  findAndPlayTone aa4
  findAndPlayTone bb4
  findAndPlayTone cc4
  findAndPlayTone dd4
  findAndPlayTone ee4
  findAndPlayTone ff4
  findAndPlayTone gg4
end




define :playNote do |tone|
  play tone
end

define :findAndPlayTone do |a|
  if(a ==  "A")
    playNote A
  end
  if(a ==  "B")
    playNote B
  end
  if(a ==  "C")
    playNote C
  end
  if(a ==  "D")
    playNote D
  end
  if(a ==  "E")
    playNote E
  end
  if(a ==  "F")
    playNote F
  end
  if(a ==  "G")
    playNote G
  end
  sleep beatTime
end
