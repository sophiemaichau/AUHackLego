beatTime = 100/60
bassOn = 1
A = :A
B = :B
C = :C
D = :D
E = :E
F = :F
G = :G

aa1,bb1,cc1,dd1,ee1,ff1,gg1,hh1 =  ""
aa2,bb2,cc2,dd2,ee2,ff2,gg2,hh2 =  ""
aa3,bb3,cc3,dd3,ee3,ff3,gg3,hh3 =  ""
aa4,bb4,cc4,dd4,ee4,ff4,gg4,hh4 =  ""

adur1, bdur1, cdur1, ddur1,edur1,fdur1,gdur1,hdur1 = 0
adur2, bdur2, cdur2, ddur2,edur2,fdur2,gdur2,hdur2 = 0
adur3, bdur3, cdur3, ddur3,edur3,fdur3,gdur3,hdur3 = 0
adur4, bdur4, cdur4, ddur4,edur4,fdur4,gdur4,hdur4 = 0


live_loop :GetNotesFromOSC do
  use_real_time
  track, useBass, a, b, c, d, e, f, g, dur, d1, d2, d3, d4, d5, d6, d7, d8 = sync "/osc/trigger/prophet"
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
    if(dur == "dur")
      adur1=d1
      bdur1=d2
      cdur1=d3
      ddur1=d4
      edur1=d5
      fdur1=d6
      gdur1=d7
      hdur1=d8
    end
    
  end
  if(track == 2)
    aa2 = a
    bb2 = b
    cc2 = c
    dd2 = d
    ee2 = e
    ff2 = f
    gg2 = g
    if(dur == "dur")
      adur2=d1
      bdur2=d2
      cdur2=d3
      ddur2=d4
      edur2=d5
      fdur2=d6
      gdur2=d7
      hdur2=d8
    end
  end
  if(track == 3)
    aa3 = a
    bb3 = b
    cc3 = c
    dd3 = d
    ee3 = e
    ff3 = f
    gg3 = g
    if(dur == "dur")
      adur3=d1
      bdur3=d2
      cdur3=d3
      ddur3=d4
      edur3=d5
      fdur3=d6
      gdur3=d7
      hdur3=d8
    end
  end
  if(track == 4)
    aa4 = a
    bb4 = b
    cc4 = c
    dd4 = d
    ee4 = e
    ff4 = f
    gg4 = g
    if(dur == "dur")
      adur4=d1
      bdur4=d2
      cdur4=d3
      ddur4=d4
      edur4=d5
      fdur4=d6
      gdur4=d7
      hdur4=d8
    end
    
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
  findAndPlayTone(aa1, adur1)
  findAndPlayTone(bb1, bdur1)
  findAndPlayTone(cc1, cdur1)
  findAndPlayTone(dd1, ddur1)
  findAndPlayTone(ee1, edur1)
  findAndPlayTone(ff1, fdur1)
  findAndPlayTone(gg1, gdur1)
  findAndPlayTone(hh1, hdur1)
end

live_loop :ChordPlayTwo do
  findAndPlayTone(aa2, adur2)
  findAndPlayTone(bb2, adur2)
  findAndPlayTone(cc2, adur2)
  findAndPlayTone(dd2, adur2)
  findAndPlayTone(ee2, adur2)
  findAndPlayTone(ff2, adur2)
  findAndPlayTone(gg2, adur2)
  findAndPlayTone(hh2, adur2)
end

live_loop :ChordPlayThree do
  findAndPlayTone(aa3, adur3)
  findAndPlayTone(bb3, adur3)
  findAndPlayTone(cc3, adur3)
  findAndPlayTone(dd3, adur3)
  findAndPlayTone(ee3, adur3)
  findAndPlayTone(ff3, adur3)
  findAndPlayTone(gg3, adur3)
  findAndPlayTone(hh3, adur3)
end

live_loop :ChordPlayFour do
  findAndPlayTone(aa4, adur4)
  findAndPlayTone(bb4, adur4)
  findAndPlayTone(cc4, adur4)
  findAndPlayTone(dd4, adur4)
  findAndPlayTone(ee4, adur4)
  findAndPlayTone(ff4, adur4)
  findAndPlayTone(gg4, adur4)
  findAndPlayTonevhh4, adur4)
end

define :playNote do |tone, dur|
  play tone, sustain: dur
end

define :findAndPlayTone do |a, dur|
  if(a ==  "A")
    playNote A, dur
  end
  if(a ==  "B")
    playNote B, dur
  end
  if(a ==  "C")
    playNote C, dur
  end
  if(a ==  "D")
    playNote D, dur
  end
  if(a ==  "E")
    playNote E, dur
  end
  if(a ==  "F")
    playNote F, dur
  end
  if(a ==  "G")
    playNote G, dur
  end
  sleep beatTime
end
