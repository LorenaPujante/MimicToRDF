
def getDurationInSeconds(start, end):
    duration = (end - start)
    duration_in_s = duration.total_seconds()

    return duration_in_s

def getDurationInMinutes(start, end):
    duration_in_s = getDurationInSeconds(start, end)
    duration_in_m = divmod(duration_in_s, 60)[0]

    return duration_in_m

def getDurationInHours(start, end):
    duration_in_s = getDurationInSeconds(start, end)
    duration_in_h = divmod(duration_in_s, 60*60)[0]

    return duration_in_h

def getDurationInDays(start, end):
    duration_in_s = getDurationInSeconds(start, end)
    duration_in_d = divmod(duration_in_s, 60*60*24)[0]

    return duration_in_d