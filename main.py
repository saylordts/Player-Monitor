from _1_Read_In_Players.readPlayers import readPlayers
from _2_Run_Scrapers.scraperCommander import scraperCommander
from _3_Write_Report.writeReport import writeReport
from _4_Send_Emails.sendEmail import sendEmail, sendFailureEmail
from _5_Save_Results.savePlayers import savePlayers
import argparse

def main(debug=True):
    print("[1/5] Reading players...")
    report = readPlayers()
    print("[1/5] Reading players... DONE")
    print()

    print("[2/5] Running scrapers...")
    report = scraperCommander(report)
    print("[2/5] Running scrapers... DONE")
    print()

    print("[3/5] Writing report...")
    report = writeReport(report)
    print("[3/5] Writing report... DONE")
    print()

    if not debug:
        print("[4/5] Saving results...")
        savePlayers(report)
        print("[4/5] Saving results... DONE")
        print()

        print("[5/5] Sending report...")
        sendEmail(report)
        print("[5/5] Sending report... DONE")
        if report.errors:
            print()
            print(f"[ERR] Sending errors ({len(report.errors)})...")
            sendFailureEmail("\n".join(report.errors))
            print(f"[ERR] Sending errors ({len(report.errors)})... DONE")
    else:
        if report.errors:
            print(f"{len(report.errors)} error(s) encountered:")
            print("\n".join(report.errors))
        else:
            print("No errors")
        return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--no-debug",
        action="store_true",
        help="Disable debug mode"
    )
    args = parser.parse_args()

    main(debug=not args.no_debug)