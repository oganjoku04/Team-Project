def sibling_spacing(individuals,families):
    """ US13  -  Birth dates of siblings should be more than 18 months space apart or
        less than 2 days apart """
    error_type = "US13"
    return_flag = True
    

    for sib in families:
        sibling_uids = sib.children
        siblings = list(indiv for indiv in individuals if indiv.uid in sibling_uids)

        sib_birthdays = sorted(siblings, key=lambda ind: ind.birthdate, reverse=False)
        i=0
        count = len(sib_birthdays)
        while i < count-1:
            diff = sib_birthdays[i+1].birthdate - sib_birthdays[i].birthdate
            if (diff > timedelta(days=2) and diff < timedelta(days=366)):
                error_descrip = "Ages in sibling weren't impossible!"
                error_location = [sib_birthdays[i+1].uid, sib_birthdays[i].uid]
                report_error(error_type, error_descrip, error_location)
                return_flag = False
            i+=1
        return return_flag

def multiple_births_less_10(individuals,families):
    """ US14  -  No more than 10 siblings should be born at the same time"""
    error_type = "US14"
    return_flag = True

    for person in families:
        sibling_uids = person.children
        siblings = list(x for x in individuals if x.uid in sibling_uids)
        sib_birthdays = []
        for sibling in siblings:
            sib_birthdays.append(sibling.birthdate)
        result_sib = Counter(sib_birthdays).most_common(1)
        for (a,b) in result_sib:
            if b > 5:
                error_descrip = "More than 10 siblings born at once"
                error_location = [person.uid]
                report_error(error_type, error_descrip, error_location)
                return_flag = False

    return return_flag


def fewer_than_fifteen_siblings(_, families):
    """ US15 - Families should not have more than 15 children - ANOMALY """
    anom_type = "US15"
    return_flag = True

    for child in families:
        if len(child.children) >= 15:
            anom_description = "Family has 15 or more siblings"
            anom_location = [child.uid]
            report_anomaly(anom_type, anom_description, anom_location)
            return_flag = False
    return return_flag

