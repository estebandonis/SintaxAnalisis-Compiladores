import sys
import pickle
from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener
from ConfRoomSchedulerLexer import ConfRoomSchedulerLexer
from ConfRoomSchedulerParser import ConfRoomSchedulerParser
from ConfRoomSchedulerListener import ConfRoomSchedulerListener

class ConfRoomSchedulerErrorListener(ErrorListener):
    def __init__(self):
        super(ConfRoomSchedulerErrorListener, self).__init__()

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise Exception(f"Syntax error at line {line}, column {column}: {msg}")

class ConfRoomScheduler(ConfRoomSchedulerListener):
    MAX_RESERVATION_HOURS = 4

    def __init__(self, reservations_file='reservations.pkl'):
        self.reservations_file = reservations_file
        self.reservations = self.load_reservations()

    def load_reservations(self):
        try:
            with open(self.reservations_file, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return {}

    def save_reservations(self):
        with open(self.reservations_file, 'wb') as f:
            pickle.dump(self.reservations, f)

    def enterReserveStat(self, ctx: ConfRoomSchedulerParser.ReserveStatContext):
        id = ctx.reserve().ID(0).getText()
        tipo = ctx.reserve().STRING(0).getText()
        date = ctx.reserve().DATE().getText()
        start_time = ctx.reserve().TIME(0).getText()
        end_time = ctx.reserve().TIME(1).getText()
        requester = ctx.reserve().ID(1).getText()
        description = ctx.reserve().STRING(1).getText() if ctx.reserve().STRING() else ""

        if self.is_valid_time(start_time, end_time):
            if not self.is_overlapping(id, date, start_time, end_time, tipo):
                # Validación de duración máxima permitida
                if self.is_within_max_duration(start_time, end_time):
                    self.reservations[(id, date, start_time, end_time, tipo)] = (requester, description)
                    self.save_reservations()
                    print(f"Reserved: {id} on {date} from {start_time} to {end_time} by {requester} with description: {description}")
                else:
                    print(f"Error: Reservation duration exceeds maximum allowed ({self.MAX_RESERVATION_HOURS} hours): {id} on {date} from {start_time} to {end_time} by {requester}")
            else:
                print(f"Error: Reservation overlaps with an existing reservation in {tipo} on {date} from {start_time} to {end_time}")
        else:
            print(f"Error: Invalid time range '{start_time} to {end_time}' for reservation on {date} by {requester}")

    def enterCancelStat(self, ctx: ConfRoomSchedulerParser.CancelStatContext):
        id = ctx.cancel().ID(0).getText()
        tipo = ctx.cancel().STRING().getText()
        date = ctx.cancel().DATE().getText()
        start_time = ctx.cancel().TIME(0).getText()
        end_time = ctx.cancel().TIME(1).getText()
        requester = ctx.cancel().ID(1).getText()
        if (id, date, start_time, end_time, tipo) in self.reservations:
            del self.reservations[(id, date, start_time, end_time, tipo)]
            self.save_reservations()
            print(f"Cancelled: {id} on {date} from {start_time} to {end_time} by {requester}")
        else:
            print(f"No reservation found to cancel: {id} on {date} from {start_time} to {end_time}")

    def enterReprogramStat(self, ctx: ConfRoomSchedulerParser.ReprogramStatContext):
        id = ctx.reprogram().ID(0).getText()
        requester = ctx.reprogram().ID(1).getText()
        newDate = ctx.reprogram().DATE().getText()
        newStart_time = ctx.reprogram().TIME(0).getText()
        newEnd_time = ctx.reprogram().TIME(1).getText()
        newTipo = ctx.reprogram().STRING().getText() if ctx.reprogram().STRING() else ""

        description = "";
        oldDate = "";
        oldStart_time = "";
        oldEnd_time = "";
        oldTipo = "";

        for res in self.reservations:
            tempRes = self.reservations[res]
            if res[0] == id and tempRes[0] == requester:
                oldDate = res[1]
                oldStart_time = res[2]
                oldEnd_time = res[3]
                oldTipo = res[4]
                description = tempRes[1]
                break

        if description == "":
            print(f"No reservation found with data: ID: {id} by {requester}")
            return
        else:
            del self.reservations[(id, oldDate, oldStart_time, oldEnd_time, oldTipo)]

        if self.is_valid_time(newStart_time, newEnd_time):
            if not self.is_overlapping(id, newDate, newStart_time, newEnd_time, newTipo):
                # Validación de duración máxima permitida
                if self.is_within_max_duration(newStart_time, newEnd_time):
                    self.reservations[(id, newDate, newStart_time, newEnd_time, newTipo)] = (requester, description)
                    self.save_reservations()
                    print(f"Reprogrammed: {id} on {newDate} from {newStart_time} to {newEnd_time} by {requester} in {newTipo} with description: {description}")
                else:
                    print(f"Error: Can't repogram reservation, duration exceeds maximum allowed ({self.MAX_RESERVATION_HOURS} hours): {id} on {newDate} from {newStart_time} to {newEnd_time} by {requester}")
            else:
                print(f"Error: Can't reprogram reservation, overlaps with an existing reservation in {newTipo} on {newDate} from {newStart_time} to {newEnd_time}")
        else:
            print(f"Error: Can't reprogram reservation, invalid time range '{newStart_time} to {newEnd_time}' for reservation on {newDate} by {requester}")

    def is_valid_time(self, start_time, end_time):
        try:
            start_hour, start_minute = map(int, start_time.split(':'))
            end_hour, end_minute = map(int, end_time.split(':'))
            if start_hour < 0 or start_hour > 23 or end_hour < 0 or end_hour > 23:
                return False
            if start_minute < 0 or start_minute > 59 or end_minute < 0 or end_minute > 59:
                return False
            if (end_hour < start_hour) or (end_hour == start_hour and end_minute <= start_minute):
                return False
            return True
        except ValueError:
            return False

    def is_overlapping(self, id, date, start_time, end_time, tipo):
        for (res_id, res_date, res_start, res_end, res_tipo) in self.reservations:
            if date == res_date and tipo == res_tipo:
                if not (end_time <= res_start or start_time >= res_end):
                    return True
        return False
    
    def is_within_max_duration(self, start_time, end_time):
        try:
            start_hour, start_minute = map(int, start_time.split(':'))
            end_hour, end_minute = map(int, end_time.split(':'))
            start_minutes = start_hour * 60 + start_minute
            end_minutes = end_hour * 60 + end_minute
            return (end_minutes - start_minutes) <= self.MAX_RESERVATION_HOURS * 60
        except ValueError:
            return False

    def list_reservations(self):
        if not self.reservations:
            print("No reservations found.")
        else:
            print("Existing reservations:")
            for (id, date, start_time, end_time, tipo), (requester, description) in self.reservations.items():
                print(f"- {id} in {tipo} on {date} from {start_time} to {end_time} by {requester} with description: {description}")

    def list_near_events(self):
        current_date = "19/06/2024"

        if not self.reservations:
            print("No reservations found.")
        else:
            print("")
            print("Near events:")
            for (id, date, start_time, end_time, tipo), (requester, description) in self.reservations.items():
                if date == current_date or (int(date[0:2]) == int(current_date[0:2]) + 1 and int(date[3:5]) == int(current_date[3:5]) and int(date[6:10]) == int(current_date[6:10])):
                    print(f"- {id} in {tipo} on {date} from {start_time} to {end_time} by {requester} with description: {description}")
            
            print("")


def main(argv):
    if len(argv) < 2:
        print("Usage: python3 DriverConfroom.py <input_file>")
        return

    input_file = argv[1]

    try:
        input_stream = FileStream(input_file)
    except IOError as e:
        print(f"Error opening file {input_file}: {e}")
        return

    lexer = ConfRoomSchedulerLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = ConfRoomSchedulerParser(stream)
    parser.removeErrorListeners()
    parser.addErrorListener(ConfRoomSchedulerErrorListener())

    tree = parser.prog()

    scheduler = ConfRoomScheduler()
    walker = ParseTreeWalker()
    walker.walk(scheduler, tree)

    # After processing commands, list existing reservations
    scheduler.list_near_events()
    scheduler.list_reservations()

if __name__ == '__main__':
    main(sys.argv)
