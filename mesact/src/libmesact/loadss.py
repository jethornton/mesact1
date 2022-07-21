import configparser

def load(parent, config):
	card = config.get('SSERIAL', 'SS_CARD')
	if card == '7i64':
		for key in config['SSERIAL']:
			value = config.get('SSERIAL', key)
			if key != 'SS_CARD':
				getattr(parent, key).setText(value)
	elif card == '7i69':
		for key in config['SSERIAL']:
			value = config.get('SSERIAL', key)
			if key != 'SS_CARD':
				getattr(parent, key).setText(value)
	elif card == '7i70':
		for key in config['SSERIAL']:
			value = config.get('SSERIAL', key)
			if key != 'SS_CARD':
				getattr(parent, key).setText(value)
	elif card == '7i71':
		for key in config['SSERIAL']:
			value = config.get('SSERIAL', key)
			if key != 'SS_CARD':
				getattr(parent, key).setText(value)
	elif card == '7i72':
		for key in config['SSERIAL']:
			value = config.get('SSERIAL', key)
			if key != 'SS_CARD':
				getattr(parent, key).setText(value)
	elif card == '7i73':
		for key in config['SSERIAL']:
			value = config.get('SSERIAL', key)
			if key != 'SS_CARD':
				getattr(parent, key).setText(value)
	elif card == '7i84':
		for key in config['SSERIAL']:
			value = config.get('SSERIAL', key)
			if key != 'SS_CARD':
				getattr(parent, key).setText(value)
	elif card == '7i87':
		for key in config['SSERIAL']:
			value = config.get('SSERIAL', key)
			if key != 'SS_CARD':
				getattr(parent, key).setText(value)

