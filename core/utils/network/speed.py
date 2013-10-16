#!/usr/bin/env python
# -*- coding: utf-8 -*-

from commands import getoutput
import curses, re, socket

dnscache = {}

def resolve( addr ):
	if not dnscache.has_key( addr ):
		try:
			dnscache[ addr ] = socket.gethostbyaddr( addr )[ 0 ]
		except ( IndexError, socket.herror, socket.error ):
			dnscache[ addr ] = addr
	return dnscache[ addr ]

# Natural sorting algorythm from http://nedbatchelder.com/blog/200712.html#e20071211T054956

def alphanum_key( s ):
	""" Turn a string into a list of string and number chunks.
		"z23a" -> ["z", 23, "a"]
	"""
	def tryint( s ):
		try:
			return int( s )
		except:
			return s
	return [ tryint( c ) for c in re.split( '(\d+)', s ) ]

# Natural sorting end

def getConns():
	f = open( '/proc/net/ip_conntrack', 'r' )
	out = [ x.strip() for x in f ]
	f.close()
	return out

def getConnsForHost( table, host ):
	return [ x for x in table if x.find( 'ESTABLISHED src=%s ' % host ) != -1 and x.find( '[ASSURED]' ) != -1 ]

def parseTable( table, upload = True ):
	out = []
	for record in table:
		if len( record ) > 0:
			record = re.split( '\s+', record.lstrip() )
			if upload:
				out.append( { 'ip' : record[ 7 ], 'bytes' : int( record[ 1 ] ) } )
			else:
				out.append( { 'ip' : record[ 8 ], 'bytes' : int( record[ 1 ] ) } )
	out.sort( key = lambda x: alphanum_key( x[ 'ip' ] ) ) # sort list by ip
	return out

def attrBySpeed( speed, limit ):
	if speed > limit * .75:
		return curses.color_pair( 3 ) | curses.A_BOLD
	elif speed > limit * .5:
		return curses.color_pair( 2 ) | curses.A_BOLD
	elif speed > limit * .25:
		return curses.color_pair( 1 ) | curses.A_BOLD
	elif speed > 1:
		return curses.A_BOLD
	return 0

def	printTable( wnd, *tables ):
	line_count = len( tables[ 0 ][ 1 ] )
	wnd.erase()
	wnd.resize( line_count + 4, wnd.getmaxyx()[ 1 ] )
	wnd.border()
	( h, w ) = wnd.getmaxyx()
	col_w = 9
	speed_cols = len( tables )
	tables = enumerate( tables )
	conns = getConns()
	for i, ( name, tab, prevtab, limit ) in tables:
		pos = w - ( ( col_w + 1 ) * ( speed_cols - i ) + 4 + 2 )
		wnd.addstr( 0, pos + col_w / 2 - len( name ) / 2, name )
		wnd.move( 1, 0 )
		total_speed = 0
		for ind, host in enumerate( tab ):
			try:
				speed = ( host[ 'bytes' ] - prevtab[ ind ][ 'bytes' ] ) / 1024.
			except ( IndexError, TypeError ): # seems like list was modified
				speed = 0
			hostconns = getConnsForHost( conns, host[ 'ip' ] )
			( y, x ) = wnd.getyx()
			attr = attrBySpeed( speed, limit )
			hostattr = attr
			wnd.attrset( attr )
			if speed > 0:
				total_speed += speed
				if speed > 1:
					wnd.addstr( y, pos + 1, '%.2f' % speed )
			#attr = attrBySpeed( upSpeed, upLimit )
			#wnd.attrset( attr )
			#hostattr = max( attr, hostattr )
			#if upSpeed > 0:
				#totalUpSpeed += upSpeed
				#if upSpeed > 1:
					#wnd.addstr( y, pos[ 'u' ] + 1, '%.2f' % upSpeed )
			wnd.attrset( hostattr )
			wnd.addstr( y, 1, host[ 'ip' ] )
			wnd.addnstr( y, 17, resolve( host[ 'ip' ] ), w - 53 )
			wnd.attrset( 0 )
			if len( hostconns ) > 0:
				wnd.addstr( y, w - 5, '%i' % len( hostconns ) )
			wnd.move( y + 1, x )
		wnd.vline( 1, pos - 1, curses.ACS_VLINE, line_count )
	wnd.addstr( h - 2, 2, 'Total: %i' % line_count )
	#wnd.addstr( h - 2, pos + 1, '%.2f' % totalDownSpeed, attrBySpeed( totalDownSpeed, downLimit ) )
	#wnd.addstr( h - 2, pos + 1, '%.2f' % totalUpSpeed, attrBySpeed( totalUpSpeed, upLimit ) )
	wnd.vline( 1, w - 7, curses.ACS_VLINE, line_count ) # before connects
	wnd.vline( 1, 16, curses.ACS_VLINE, line_count ) # after ip
	wnd.hline( h - 3, 1, curses.ACS_HLINE, w - 2 ) # bottom line

def main( scr ):
	prevul_total, prevul_mtc, prevul_star = None, None, None
	prevdl_total, prevdl_mtc, prevdl_star = [], [], []
	curses.init_pair( 1, curses.COLOR_GREEN, curses.COLOR_BLACK )
	curses.init_pair( 2, curses.COLOR_YELLOW, curses.COLOR_BLACK )
	curses.init_pair( 3, curses.COLOR_RED, curses.COLOR_BLACK )
	speedWnd = curses.newpad( 10, 110 )
	while True:
		dl_total = parseTable( getoutput( 'iptables -xnvL count_in | tail -n+3' ).split( '\n' ), False )
		dl_mtc = parseTable( getoutput( 'iptables -xnvL count_mtc_in | tail -n+3' ).split( '\n' ), False )
		#dl_star = parseTable( getoutput( 'iptables -xnvL count_star_in | tail -n+3' ).split( '\n' ), False )
		ul_total = parseTable( getoutput( 'iptables -xnvL count_out | tail -n+3' ).split( '\n' ) )
		ul_mtc = parseTable( getoutput( 'iptables -xnvL count_mtc_out | tail -n+3' ).split( '\n' ) )
		#ul_star = parseTable( getoutput( 'iptables -xnvL count_star_out | tail -n+3' ).split( '\n' ) )
		printTable( speedWnd,
			( 'D/total', dl_total, prevdl_total, 4000 ),
			( 'U/total', ul_total, prevul_total, 3100 ),
			( 'D/mtc', dl_mtc, prevdl_mtc, 2000 ),
			( 'U/mtc', ul_mtc, prevul_mtc, 100 ),
#			( 'D/star', dl_star, prevdl_star, 3000 ),
#			( 'U/star', ul_star, prevul_star, 3000 )
		)
		prevdl_total, prevul_total = dl_total, ul_total
		prevdl_mtc, prevul_mtc = dl_mtc, ul_mtc
#		prevdl_star, prevul_star = dl_star, ul_star
		scr.erase()
		scr.refresh()
		( sh, sw ) = scr.getmaxyx()
		( h, w ) = speedWnd.getmaxyx()
		try:
			speedWnd.refresh( 0, 0, 0, 0, min( h, sh ) - 1, min( w, sw ) - 1 )
		except curses.error:
			pass
		for i in xrange( 10 ):
			curses.napms( 100 )

curses.wrapper( main )
