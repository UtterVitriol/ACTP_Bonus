## Create a Python program that represents the state machine for a laundromat washing machine.
### Your machine must include the following states:

    door open, unlocked, machine off
    door closed, unlocked, machine off
    door closed, locked, machine on
    fill cycle (variable levels)
    wash cycle (variable time lengths)
    rinse cycle (variable iterations)
    spin cycle (variable iterations)

#### Your machine must meet the following requirements:

#### (1 pt) must require a minimum of $2.00 to operate a standard 30-minute run (includes the regular fill, regular wash, single-rinse, and single-spin cycles)

#### Can take an additional $0.50-$4.00 in $0.25 intervals to increase cycles - see add-ons below:
#### (1 pt) fill cycles can range from light->normal->heavy with light receiving zero monetary discount, but heavy requiring an additional $0.50 to begin a run
     total run time changes include: light -=2min, regular == 5min, heavy +=3min
#### (1 pt) wash cycles can range from light->normal->heavy with light receiving zero monetary discount, but heavy requiring an additional $1.50 to begin a run
    total run time changes include: light -=5min, regular == 10min, heavy +=7min
#### (1 pt) rinse cycles can range from single->double with double requiring an additional $1.25 to begin a run
    total run time changes include: single == 10min, double +=5min
#### (1 pt) spin cycles can range from single->double with double requiring an additional $0.75 to begin run
        total run time changes include: single == 5min, double +=6min
#### (1 pt) must require a fill, wash, rinse, and spin cycle be selected before starting a run
#### (1 pt) must have a 'start' button to toggle run on - button should not be able to be toggled 'off' during a run, button should toggle 'on' after a run completes
#### (1 pt) must require door to be closed, door to be locked, cycles to be selected, and $ to be deposited before 'start' can be pressed to trigger the run to begin
#### (1 pt) must have a minute timer to track run time/progress with 0min triggering the 'start' button 'on'
#### (1 pt) must have either a 'light' or 'message' indicating the current cycle being executed during the run
#### (1 pt) must have a the ability to add $ at any time during the run to adjust current/future cycles time, must not allow past/completed cycle times to be adjusted
#### (1 pt) must log the following 1. lifetime runtime (X.X hrs format), 2. lifetime runs (whole integer format), 3. lifetime deposits ($X.XX format)

Please upload your script, as this problem will be hand-graded by the instructor.
