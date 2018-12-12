import pytest
import random
from person import Person
from simulation import Simulation as simulation
from virus import Virus as virus


class Logger:
    ''' Utility class responsible for logging all interactions during the simulation. '''

    def __init__(self, file_name):
        self.file_name = file_name

    def write_metadata(self, pop_size, vacc_percentage, virus_name, mortality_rate, basic_repro_num):
        '''
        The simulation class should use this method immediately to log the specific
        parameters of the simulation as the first line of the file.
        '''
        data = ["=====================\nStats of the virus\n---------------------\nVirus name: {} \n".format(
            virus_name), "Population size: {} \n".format(pop_size), "Vaccination Percentage: {} \n".format(vacc_percentage), "Mortality Rate: {}\n".format(mortality_rate), "Basic reproduction number: {}\n=====================\n".format(basic_repro_num)]

        with open(self.file_name, "w") as file:
            file.writelines(data)

    def append_interaction(self, data, mode):
        with open("interactions.txt", mode) as file:
            file.writelines(data)

    def log_interaction(self, person, random_person, random_sick_person=None,
                        random_vacc_person=None, did_infect=None):
        '''
        The Simulation object should use this method to log every interaction
        a sick person has during each time step.
        The format of the log should be: "{person.ID} infects {random_person.ID} \n"
        or the other edge cases:
        "{person.ID} didn't infect {random_person.ID} because {'vaccinated' or 'already sick'} \n"
        '''
        if person.infection == virus and random_person.infection == virus:
            did_infect = False
            self.append_interaction(["Person {} didn't infect Person {} because they are already sick.\n".format(
                person._id, random_person._id)], "a")
        elif person.infection == virus and random_person.is_vaccinated == True:
            did_infect = False
            self.append_interaction(
                ["Person {} did not infect Person{} because they are vaccinated".format(person._id, random_person._id)], "a")
        elif person.infection == virus and random_person.is_vaccinated == False:
            num = random.random()
            # FIXME: Future EB+WILL? Why does virus not work in here?
            if num < virus.repro_rate:
                random_person.infection = virus
                did_infect = True
                self.append_interaction(["Person {} infected Person {} because they weren't vaccinated\n".format(
                    person._id, random_person._id)], "a")

            else:
                self.append_interaction(["Person {} did not infect Person {} because they got luckyyyyy\n".format(
                    person._id, random_person._id)], "a")
                did_infect = False
        else:
            pass

        # TODO: Finish this method. Think about how the booleans passed (or not passed)
        # represent all the possible edge cases. Use the values passed along with each person,
        # along with whether they are sick or vaccinated when they interact to determine
        # exactly what happened in the interaction and create a String, and write to your logfile.

    def log_infection_survival(self, person, did_die_from_infection):
        ''' The Simulation object uses this method to log the results of every
        call of a Person object's .resolve_infection() method.
        '''
        with open(self.file_name, "a") as file:
            if person.is_alive:
                file.writelines(
                    ["{} survived infection \n".format(person._id)])
                did_die_from_infection = False
            else:
                file.writelines(
                    ["{} died from infection \n".format(person._id)])
                did_die_from_infection = True

    def log_time_step(self, time_step_number):
        with open(self.file_name, "a") as file:
            file.writelines(["Time step number {} ended, beginning {} \n".format(
                time_step_number, time_step_number + 1)])


# FIXME: Add asserts
def test_write_metadata():
    logger = Logger("interactions.txt")
    logger.write_metadata(100000, 0.4, "Snapple", 0.2, 0.3)


def test_log_time_step():
    logger = Logger("interactions.txt")
    logger.log_time_step(10)


def test_log_infection_survival():
    from person import Person
    from virus import Virus
    logger = Logger("interactions.txt")
    virus = Virus("Snapple", 0.2, 0.4)
    person = Person(1, True, virus)


def test_log_interaction():
    from person import Person
    from virus import Virus
    virus = Virus("Snapple", 0.2, 0.4)
    person = Person(1, False, virus)
    random_person = Person(2, False)
    logger = Logger("test.txt")
    if person.infection == virus and random_person.infection == virus:
        logger.append_interaction(["Person {} did not infect Person {} because they are vaccinated\n".format(
            person._id, random_person._id)], "a")
    elif person.infection == virus and random_person.is_vaccinated:
        logger.append_interaction(["Person {} did not infect Person {} because they are vaccinated\n".format(
            person._id, random_person._id)], "a")

    elif person.infection == virus and random_person.is_vaccinated == False:
        num = random.random()
        logger.append_interaction(["Random number {} - Virus Repro Rate {}\n".format(
            num, virus.repro_rate)], "a")
        if num < virus.repro_rate:
            random_person.infection = virus
            logger.append_interaction(["Person {} infected Person {} because they weren't vaccinated\n".format(
                person._id, random_person._id)], "a")
            did_infect = True
        else:
            logger.append_interaction(["Person {} did not infect Person {} because they got luckyyyyy\n".format(
                person._id, random_person._id)], "a")
            did_infect = False
    else:
        pass
