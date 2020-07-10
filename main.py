import discord
import google.auth
from googleapiclient import discovery

SHEET_ID = '1Ocg86emlSVShZZQ-GPuS6YZ6miGotZZPRgKdlUlRCvw'

client = discord.Client()

creds, project = google.auth.default(scopes=['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive.file'])
svc = discovery.build('sheets', 'v4', credentials=creds)
sheets = svc.spreadsheets()
print(project)


@client.event
async def on_ready():
	print('logged in as {0.user}'.format(client))

@client.event
async def on_member_join(member):
	await add_member(member)

@client.event
async def on_member_remove(member):
	await delete_member(member)

@client.event
async def on_guild_join(guild):
	for member in guild.members:
		await add_member(member)

async def add_member(member):
	req = sheets.batchUpdate(spreadsheetId=SHEET_ID, body={
		'includeSpreadsheetInResponse': False,
		'requests': [{
			'appendCells': {
				'sheetId': 0,
				'fields': 'userEnteredValue',
				'rows': [{
					'values': [{
						'userEnteredValue': {
							"stringValue": str(member)
						}
					}]
				}]
			}
		}]
	})

	req.execute()

async def delete_member(member):
	req = sheets.values().get(spreadsheetId=SHEET_ID, range='A:A', majorDimension='COLUMNS')
	res = req.execute()
	arr = res["values"][0]
	i = arr.index(str(member))

	req = sheets.batchUpdate(spreadsheetId=SHEET_ID, body={
		'includeSpreadsheetInResponse': False,
		'requests': [{
			'deleteDimension': {
				'range': {
					'sheetId': 0,
					'dimension': 'ROWS',
					'startIndex': i,
					'endIndex': i+1
				}
			}
		}]
	})

	req.execute()

client.run('NzMwODgxMzUyMTMxNDEyMDY4.XweAcQ.Tk6euolaUe43CeGQngEwbcZPZk4')