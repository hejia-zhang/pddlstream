(define (problem rm-100-2-25-5)
    (:domain risk)
    (:objects o0 o1 o2 o3 o4 o5 o6 o7 o8 o9 o10 o11 o12 o13 o14 o15 o16 o17 o18 o19 o20 o21 o22 o23 o24 o25 o26 o27 o28 o29 o30 o31 o32 o33 o34 o35 o36 o37 o38 o39 o40 o41 o42 o43 o44 o45 o46 o47 o48 o49 o50 o51 o52 o53 o54 o55 o56 o57 o58 o59 o60 o61 o62 o63 o64 o65 o66 o67 o68 o69 o70 o71 o72 o73 o74 o75 o76 o77 o78 o79 o80 o81 o82 o83 o84 o85 o86 o87 o88 o89 o90 o91 o92 o93 o94 o95 o96 o97 o98 o99 dummy)
    (:init
        (SOURCE o76)
        (SOURCE o93)
        (TARGET o13)
        (TARGET o37)
        (TARGET o41)
        (TARGET o50)
        (TARGET o55)
        (TARGET o63)
        (TARGET o64)
        (TARGET o73)
        (TARGET o80)
        (TARGET o88)
        (TARGET o89)
        (TARGET o95)
        (TARGET o96)
        (TARGET o57)
        (TARGET o5)
        (TARGET o74)
        (TARGET o75)
        (TARGET o51)
        (TARGET o92)
        (TARGET o2)
        (TARGET o16)
        (TARGET o61)
        (TARGET o28)
        (TARGET o98)
        (TARGET o36)
        (POI o17)
        (POI o62)
        (POI o50)
        (POI o55)
        (POI o18)
        (CONNECTED o0 o3)
        (CONNECTED o0 o26)
        (CONNECTED o0 o34)
        (CONNECTED o0 o88)
        (CONNECTED o1 o4)
        (CONNECTED o1 o8)
        (CONNECTED o1 o16)
        (CONNECTED o1 o18)
        (CONNECTED o1 o30)
        (CONNECTED o1 o44)
        (CONNECTED o1 o46)
        (CONNECTED o1 o50)
        (CONNECTED o1 o78)
        (CONNECTED o2 o0)
        (CONNECTED o2 o1)
        (CONNECTED o2 o3)
        (CONNECTED o2 o6)
        (CONNECTED o2 o7)
        (CONNECTED o2 o14)
        (CONNECTED o2 o19)
        (CONNECTED o2 o22)
        (CONNECTED o2 o32)
        (CONNECTED o2 o47)
        (CONNECTED o2 o63)
        (CONNECTED o2 o64)
        (CONNECTED o2 o74)
        (CONNECTED o3 o5)
        (CONNECTED o3 o61)
        (CONNECTED o4 o1)
        (CONNECTED o4 o2)
        (CONNECTED o4 o6)
        (CONNECTED o4 o10)
        (CONNECTED o4 o12)
        (CONNECTED o4 o13)
        (CONNECTED o4 o54)
        (CONNECTED o5 o2)
        (CONNECTED o5 o8)
        (CONNECTED o5 o45)
        (CONNECTED o5 o55)
        (CONNECTED o5 o70)
        (CONNECTED o5 o85)
        (CONNECTED o5 o89)
        (CONNECTED o6 o79)
        (CONNECTED o7 o1)
        (CONNECTED o7 o25)
        (CONNECTED o7 o41)
        (CONNECTED o8 o33)
        (CONNECTED o8 o50)
        (CONNECTED o8 o83)
        (CONNECTED o9 o2)
        (CONNECTED o9 o4)
        (CONNECTED o9 o13)
        (CONNECTED o9 o15)
        (CONNECTED o9 o29)
        (CONNECTED o9 o37)
        (CONNECTED o9 o84)
        (CONNECTED o9 o96)
        (CONNECTED o10 o1)
        (CONNECTED o10 o81)
        (CONNECTED o11 o1)
        (CONNECTED o11 o6)
        (CONNECTED o12 o4)
        (CONNECTED o12 o6)
        (CONNECTED o12 o90)
        (CONNECTED o14 o9)
        (CONNECTED o14 o40)
        (CONNECTED o14 o48)
        (CONNECTED o14 o73)
        (CONNECTED o15 o2)
        (CONNECTED o15 o16)
        (CONNECTED o15 o39)
        (CONNECTED o15 o65)
        (CONNECTED o15 o97)
        (CONNECTED o16 o24)
        (CONNECTED o16 o73)
        (CONNECTED o17 o12)
        (CONNECTED o17 o5)
        (CONNECTED o18 o5)
        (CONNECTED o18 o49)
        (CONNECTED o19 o8)
        (CONNECTED o20 o16)
        (CONNECTED o20 o17)
        (CONNECTED o20 o23)
        (CONNECTED o20 o89)
        (CONNECTED o21 o8)
        (CONNECTED o21 o1)
        (CONNECTED o21 o24)
        (CONNECTED o22 o1)
        (CONNECTED o22 o37)
        (CONNECTED o22 o64)
        (CONNECTED o22 o94)
        (CONNECTED o23 o5)
        (CONNECTED o23 o27)
        (CONNECTED o23 o28)
        (CONNECTED o23 o55)
        (CONNECTED o23 o67)
        (CONNECTED o24 o71)
        (CONNECTED o25 o13)
        (CONNECTED o25 o43)
        (CONNECTED o25 o72)
        (CONNECTED o26 o7)
        (CONNECTED o27 o17)
        (CONNECTED o28 o1)
        (CONNECTED o28 o68)
        (CONNECTED o29 o2)
        (CONNECTED o30 o13)
        (CONNECTED o31 o0)
        (CONNECTED o31 o16)
        (CONNECTED o32 o21)
        (CONNECTED o32 o36)
        (CONNECTED o33 o1)
        (CONNECTED o34 o9)
        (CONNECTED o34 o42)
        (CONNECTED o34 o63)
        (CONNECTED o34 o95)
        (CONNECTED o35 o16)
        (CONNECTED o35 o20)
        (CONNECTED o36 o13)
        (CONNECTED o38 o25)
        (CONNECTED o38 o6)
        (CONNECTED o38 o41)
        (CONNECTED o39 o4)
        (CONNECTED o40 o16)
        (CONNECTED o42 o27)
        (CONNECTED o43 o41)
        (CONNECTED o43 o80)
        (CONNECTED o44 o33)
        (CONNECTED o44 o85)
        (CONNECTED o45 o12)
        (CONNECTED o46 o24)
        (CONNECTED o47 o14)
        (CONNECTED o48 o44)
        (CONNECTED o48 o95)
        (CONNECTED o49 o5)
        (CONNECTED o49 o98)
        (CONNECTED o51 o29)
        (CONNECTED o51 o37)
        (CONNECTED o52 o25)
        (CONNECTED o52 o14)
        (CONNECTED o53 o48)
        (CONNECTED o53 o1)
        (CONNECTED o54 o23)
        (CONNECTED o54 o80)
        (CONNECTED o54 o87)
        (CONNECTED o56 o51)
        (CONNECTED o56 o7)
        (CONNECTED o57 o0)
        (CONNECTED o57 o2)
        (CONNECTED o58 o31)
        (CONNECTED o58 o15)
        (CONNECTED o59 o18)
        (CONNECTED o59 o23)
        (CONNECTED o60 o40)
        (CONNECTED o60 o49)
        (CONNECTED o61 o0)
        (CONNECTED o61 o88)
        (CONNECTED o62 o9)
        (CONNECTED o62 o4)
        (CONNECTED o65 o62)
        (CONNECTED o66 o10)
        (CONNECTED o66 o63)
        (CONNECTED o67 o52)
        (CONNECTED o68 o16)
        (CONNECTED o68 o86)
        (CONNECTED o69 o2)
        (CONNECTED o69 o37)
        (CONNECTED o70 o41)
        (CONNECTED o70 o75)
        (CONNECTED o71 o9)
        (CONNECTED o72 o2)
        (CONNECTED o74 o26)
        (CONNECTED o75 o28)
        (CONNECTED o76 o0)
        (CONNECTED o76 o41)
        (CONNECTED o77 o35)
        (CONNECTED o77 o12)
        (CONNECTED o78 o2)
        (CONNECTED o79 o58)
        (CONNECTED o79 o92)
        (CONNECTED o81 o39)
        (CONNECTED o82 o59)
        (CONNECTED o82 o23)
        (CONNECTED o83 o14)
        (CONNECTED o84 o64)
        (CONNECTED o85 o99)
        (CONNECTED o86 o4)
        (CONNECTED o87 o2)
        (CONNECTED o90 o77)
        (CONNECTED o91 o16)
        (CONNECTED o91 o11)
        (CONNECTED o92 o0)
        (CONNECTED o92 o79)
        (CONNECTED o93 o48)
        (CONNECTED o93 o72)
        (CONNECTED o94 o6)
        (CONNECTED o96 o57)
        (CONNECTED o96 o9)
        (CONNECTED o97 o79)
        (CONNECTED o98 o77)
        (CONNECTED o99 o17)
        (DISCARD_AFTER o17 dummy)
        (DISCARD_AFTER o62 o17)
        (DISCARD_AFTER o50 o62)
        (DISCARD_AFTER o55 o50)
        (DISCARD_AFTER o18 o55)
        (= (total-cost) 0)
        (= (discard-cost) 100)
        (= (starting-cost o76) 0)
        (= (starting-cost o93) 0)
        (= (connected-cost o0 o3) 10)
        (= (connected-cost o0 o26) 10)
        (= (connected-cost o0 o34) 10)
        (= (connected-cost o0 o88) 10)
        (= (connected-cost o1 o4) 10)
        (= (connected-cost o1 o8) 10)
        (= (connected-cost o1 o16) 10)
        (= (connected-cost o1 o18) 10)
        (= (connected-cost o1 o30) 10)
        (= (connected-cost o1 o44) 10)
        (= (connected-cost o1 o46) 10)
        (= (connected-cost o1 o50) 10)
        (= (connected-cost o1 o78) 30)
        (= (connected-cost o2 o0) 10)
        (= (connected-cost o2 o1) 10)
        (= (connected-cost o2 o3) 10)
        (= (connected-cost o2 o6) 10)
        (= (connected-cost o2 o7) 10)
        (= (connected-cost o2 o14) 30)
        (= (connected-cost o2 o19) 10)
        (= (connected-cost o2 o22) 10)
        (= (connected-cost o2 o32) 10)
        (= (connected-cost o2 o47) 10)
        (= (connected-cost o2 o63) 10)
        (= (connected-cost o2 o64) 10)
        (= (connected-cost o2 o74) 30)
        (= (connected-cost o3 o5) 10)
        (= (connected-cost o3 o61) 10)
        (= (connected-cost o4 o1) 10)
        (= (connected-cost o4 o2) 10)
        (= (connected-cost o4 o6) 30)
        (= (connected-cost o4 o10) 10)
        (= (connected-cost o4 o12) 30)
        (= (connected-cost o4 o13) 10)
        (= (connected-cost o4 o54) 10)
        (= (connected-cost o5 o2) 10)
        (= (connected-cost o5 o8) 30)
        (= (connected-cost o5 o45) 10)
        (= (connected-cost o5 o55) 10)
        (= (connected-cost o5 o70) 10)
        (= (connected-cost o5 o85) 30)
        (= (connected-cost o5 o89) 10)
        (= (connected-cost o6 o79) 30)
        (= (connected-cost o7 o1) 10)
        (= (connected-cost o7 o25) 10)
        (= (connected-cost o7 o41) 10)
        (= (connected-cost o8 o33) 30)
        (= (connected-cost o8 o50) 10)
        (= (connected-cost o8 o83) 10)
        (= (connected-cost o9 o2) 10)
        (= (connected-cost o9 o4) 10)
        (= (connected-cost o9 o13) 10)
        (= (connected-cost o9 o15) 10)
        (= (connected-cost o9 o29) 10)
        (= (connected-cost o9 o37) 10)
        (= (connected-cost o9 o84) 10)
        (= (connected-cost o9 o96) 10)
        (= (connected-cost o10 o1) 10)
        (= (connected-cost o10 o81) 10)
        (= (connected-cost o11 o1) 10)
        (= (connected-cost o11 o6) 10)
        (= (connected-cost o12 o4) 10)
        (= (connected-cost o12 o6) 10)
        (= (connected-cost o12 o90) 10)
        (= (connected-cost o14 o9) 10)
        (= (connected-cost o14 o40) 10)
        (= (connected-cost o14 o48) 10)
        (= (connected-cost o14 o73) 30)
        (= (connected-cost o15 o2) 10)
        (= (connected-cost o15 o16) 10)
        (= (connected-cost o15 o39) 10)
        (= (connected-cost o15 o65) 10)
        (= (connected-cost o15 o97) 10)
        (= (connected-cost o16 o24) 10)
        (= (connected-cost o16 o73) 30)
        (= (connected-cost o17 o12) 30)
        (= (connected-cost o17 o5) 10)
        (= (connected-cost o18 o5) 10)
        (= (connected-cost o18 o49) 10)
        (= (connected-cost o19 o8) 10)
        (= (connected-cost o20 o16) 30)
        (= (connected-cost o20 o17) 10)
        (= (connected-cost o20 o23) 10)
        (= (connected-cost o20 o89) 10)
        (= (connected-cost o21 o8) 30)
        (= (connected-cost o21 o1) 10)
        (= (connected-cost o21 o24) 10)
        (= (connected-cost o22 o1) 10)
        (= (connected-cost o22 o37) 30)
        (= (connected-cost o22 o64) 10)
        (= (connected-cost o22 o94) 30)
        (= (connected-cost o23 o5) 10)
        (= (connected-cost o23 o27) 10)
        (= (connected-cost o23 o28) 10)
        (= (connected-cost o23 o55) 10)
        (= (connected-cost o23 o67) 30)
        (= (connected-cost o24 o71) 10)
        (= (connected-cost o25 o13) 10)
        (= (connected-cost o25 o43) 30)
        (= (connected-cost o25 o72) 30)
        (= (connected-cost o26 o7) 30)
        (= (connected-cost o27 o17) 10)
        (= (connected-cost o28 o1) 30)
        (= (connected-cost o28 o68) 10)
        (= (connected-cost o29 o2) 10)
        (= (connected-cost o30 o13) 30)
        (= (connected-cost o31 o0) 10)
        (= (connected-cost o31 o16) 10)
        (= (connected-cost o32 o21) 30)
        (= (connected-cost o32 o36) 10)
        (= (connected-cost o33 o1) 10)
        (= (connected-cost o34 o9) 30)
        (= (connected-cost o34 o42) 10)
        (= (connected-cost o34 o63) 10)
        (= (connected-cost o34 o95) 10)
        (= (connected-cost o35 o16) 10)
        (= (connected-cost o35 o20) 10)
        (= (connected-cost o36 o13) 10)
        (= (connected-cost o38 o25) 30)
        (= (connected-cost o38 o6) 10)
        (= (connected-cost o38 o41) 30)
        (= (connected-cost o39 o4) 30)
        (= (connected-cost o40 o16) 10)
        (= (connected-cost o42 o27) 30)
        (= (connected-cost o43 o41) 10)
        (= (connected-cost o43 o80) 10)
        (= (connected-cost o44 o33) 10)
        (= (connected-cost o44 o85) 10)
        (= (connected-cost o45 o12) 10)
        (= (connected-cost o46 o24) 10)
        (= (connected-cost o47 o14) 30)
        (= (connected-cost o48 o44) 10)
        (= (connected-cost o48 o95) 10)
        (= (connected-cost o49 o5) 10)
        (= (connected-cost o49 o98) 10)
        (= (connected-cost o51 o29) 10)
        (= (connected-cost o51 o37) 10)
        (= (connected-cost o52 o25) 10)
        (= (connected-cost o52 o14) 30)
        (= (connected-cost o53 o48) 10)
        (= (connected-cost o53 o1) 10)
        (= (connected-cost o54 o23) 10)
        (= (connected-cost o54 o80) 30)
        (= (connected-cost o54 o87) 10)
        (= (connected-cost o56 o51) 10)
        (= (connected-cost o56 o7) 10)
        (= (connected-cost o57 o0) 10)
        (= (connected-cost o57 o2) 30)
        (= (connected-cost o58 o31) 10)
        (= (connected-cost o58 o15) 10)
        (= (connected-cost o59 o18) 10)
        (= (connected-cost o59 o23) 10)
        (= (connected-cost o60 o40) 30)
        (= (connected-cost o60 o49) 10)
        (= (connected-cost o61 o0) 10)
        (= (connected-cost o61 o88) 10)
        (= (connected-cost o62 o9) 30)
        (= (connected-cost o62 o4) 10)
        (= (connected-cost o65 o62) 10)
        (= (connected-cost o66 o10) 10)
        (= (connected-cost o66 o63) 30)
        (= (connected-cost o67 o52) 30)
        (= (connected-cost o68 o16) 10)
        (= (connected-cost o68 o86) 10)
        (= (connected-cost o69 o2) 10)
        (= (connected-cost o69 o37) 10)
        (= (connected-cost o70 o41) 10)
        (= (connected-cost o70 o75) 10)
        (= (connected-cost o71 o9) 10)
        (= (connected-cost o72 o2) 10)
        (= (connected-cost o74 o26) 10)
        (= (connected-cost o75 o28) 10)
        (= (connected-cost o76 o0) 10)
        (= (connected-cost o76 o41) 10)
        (= (connected-cost o77 o35) 30)
        (= (connected-cost o77 o12) 30)
        (= (connected-cost o78 o2) 10)
        (= (connected-cost o79 o58) 30)
        (= (connected-cost o79 o92) 30)
        (= (connected-cost o81 o39) 10)
        (= (connected-cost o82 o59) 10)
        (= (connected-cost o82 o23) 10)
        (= (connected-cost o83 o14) 10)
        (= (connected-cost o84 o64) 10)
        (= (connected-cost o85 o99) 10)
        (= (connected-cost o86 o4) 10)
        (= (connected-cost o87 o2) 10)
        (= (connected-cost o90 o77) 10)
        (= (connected-cost o91 o16) 10)
        (= (connected-cost o91 o11) 10)
        (= (connected-cost o92 o0) 10)
        (= (connected-cost o92 o79) 30)
        (= (connected-cost o93 o48) 10)
        (= (connected-cost o93 o72) 10)
        (= (connected-cost o94 o6) 10)
        (= (connected-cost o96 o57) 10)
        (= (connected-cost o96 o9) 10)
        (= (connected-cost o97 o79) 10)
        (= (connected-cost o98 o77) 10)
        (= (connected-cost o99 o17) 10)
        (considered dummy)
    )
    (:goal (and
        (__goal-achieved)
        (considered o17)
        (considered o62)
        (considered o50)
        (considered o55)
        (considered o18)
        )
    )
    (:metric minimize (total-cost))
)
