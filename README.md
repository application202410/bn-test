
## Installation and Running the Project
TODO


## Approach
The brief (and my conversation) stressed the need to keep this simple, so I'm going to start by getting all the basics done, build and the recommendation algorithm and then see how much time I hacve left to play with it and improve it.

I've divided this into a few key tasks:
- Project setup and basic 'Hello World' run instructions
- General project structure
- Download and parse phase
- Person-Job matching phase
- Output


### Project setup
I've reviewed enough developer tests to know how much I appreciate decent, clear and fuss-free instructions to get the code running. For nice, universal ease the approach I'm going with is:
- devcontainer file for development
- simple Dockerfile for 'production' run
- Docker compose file just to save on running Docker commands: I want this to be a one-command launch.

This feels like a good balance between simplicity of use and setup.

### General project structure
Whilst there's an appeal to showing off here and splitting the project into multiple pieces - e.g. a Recommendation API that ingests data and responds to POST requests for individual people, I think that's probably outside the scope of this task.

Keeping a clear focus on the end goal, I'm going to have:
- A main executable script
- A downloader that does all the outwards requests and parses data
- An interchangeable recommendations engine
    - This will take all the parsed data and returns a map of Person->Jobs.
    - Interchangeable so I can play around with different versions as drop-in replacements.
- A formatter that takes the mapped recommendations and writes output
    - This could e.g. write to a DB, serialise to JSON, etc.
    - But here it will simply print to console.
- Tests
    - I'm not going to work towards 100% coverage, given time constraints but will write tests mainly to help me as I write new code.

### Download and parse phase
I've kept this very simple and not really added much error handling or validation. Even with the presumption that this is a trusted, internal API, there really ought to be _some_ handling of errors. I've not spent any time doing that here - these will simply fall over if the input data is broken.

### Matching Phase
This is obviously the heart of the problem. I've created a structure that allows for swapping in new engines to try new versions.

Approaches:
#### Dummy Matcher
This is just an available jobs search really. It gives everyone every job.

#### KeyWord Matcher
I massively underestimated how long this would take to do, which prevented me from getting on to the fun part (see next matcher).

It takes a step-by-step approach:
- Extract employment type from job (currently just "is it an internship")
- Extract high-level category from job (using manual keyword mapping)
- Now loop through members, trying each job for them:
    - If they specifiy internship, only give them internships
    - If they specify a category, only give them matching category jobs
    



### Output
As per the brief, this is very simple. I've split it out as a 'formatter' so that it could be easily replaced by something more sophisticated but not done anything more clever than that. this implementation simply loops through the members and prints out an alphabetical list of jobs for them. 

 ## Discussion

 > a brief acknowledgement of the challenges posed by the problem and its domain and a discussion of the choices you've made and your reasons.