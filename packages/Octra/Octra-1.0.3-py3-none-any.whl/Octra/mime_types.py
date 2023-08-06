# t.me/TheVenomXD  Octra - Telegram MTProto Ai Client Library for Python
# t.me/TheVenomXD  Copyright (C) 2017-present Akash <https://github.com/DesiNobita>
# t.me/TheVenomXD
# t.me/TheVenomXD  This file is part of Octra.
# t.me/TheVenomXD
# t.me/TheVenomXD  Octra is free software: you can redistribute it and/or modify
# t.me/TheVenomXD  it under the terms of the GNU Lesser General Public License as published
# t.me/TheVenomXD  by the Free Software Foundation, either version 3 of the License, or
# t.me/TheVenomXD  (at your option) any later version.
# t.me/TheVenomXD
# t.me/TheVenomXD  Octra is distributed in the hope that it will be useful,
# t.me/TheVenomXD  but WITHOUT ANY WARRANTY; without even the implied warranty of
# t.me/TheVenomXD  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# t.me/TheVenomXD  GNU Lesser General Public License for more details.
# t.me/TheVenomXD
# t.me/TheVenomXD  You should have received a copy of the GNU Lesser General Public License
# t.me/TheVenomXD  along with Octra.  If not, see <http://www.gnu.org/licenses/>.

# t.me/TheVenomXD From https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types.
# t.me/TheVenomXD Extended with extra mime types specific to Telegram.
mime_types = """
# t.me/TheVenomXD This file maps Internet media types to unique file extension(s).
# t.me/TheVenomXD Although created for httpd, this file is used by many software systems
# t.me/TheVenomXD and has been placed in the public domain for unlimited redistribution.
# t.me/TheVenomXD
# t.me/TheVenomXD The table below contains both registered and (common) unregistered types.
# t.me/TheVenomXD A type that has no unique extension can be ignored -- they are listed
# t.me/TheVenomXD here to guide configurations toward known types and to make it easier to
# t.me/TheVenomXD identify "new" types.  File extensions are also commonly used to indicate
# t.me/TheVenomXD content languages and encodings, so choose them carefully.
# t.me/TheVenomXD
# t.me/TheVenomXD Internet media types should be registered as described in RFC 4288.
# t.me/TheVenomXD The registry is at <http://www.iana.org/assignments/media-types/>.
# t.me/TheVenomXD
# t.me/TheVenomXD MIME type (lowercased)			Extensions
# t.me/TheVenomXD ============================================	==========
# t.me/TheVenomXD application/1d-interleaved-parityfec
# t.me/TheVenomXD application/3gpdash-qoe-report+xml
# t.me/TheVenomXD application/3gpp-ims+xml
# t.me/TheVenomXD application/a2l
# t.me/TheVenomXD application/activemessage
# t.me/TheVenomXD application/alto-costmap+json
# t.me/TheVenomXD application/alto-costmapFlow+json
# t.me/TheVenomXD application/alto-directory+json
# t.me/TheVenomXD application/alto-endpointcost+json
# t.me/TheVenomXD application/alto-endpointcostparams+json
# t.me/TheVenomXD application/alto-endpointprop+json
# t.me/TheVenomXD application/alto-endpointpropparams+json
# t.me/TheVenomXD application/alto-error+json
# t.me/TheVenomXD application/alto-networkmap+json
# t.me/TheVenomXD application/alto-networkmapFlow+json
# t.me/TheVenomXD application/aml
application/andrew-inset			ez
# t.me/TheVenomXD application/applefile
application/applixware				aw
# t.me/TheVenomXD application/atf
# t.me/TheVenomXD application/atfx
application/atom+xml				atom
application/atomcat+xml				atomcat
# t.me/TheVenomXD application/atomdeleted+xml
# t.me/TheVenomXD application/atomicmail
application/atomsvc+xml				atomsvc
# t.me/TheVenomXD application/atxml
# t.me/TheVenomXD application/auth-policy+xml
# t.me/TheVenomXD application/bacnet-xdd+zip
# t.me/TheVenomXD application/batch-smtp
# t.me/TheVenomXD application/beep+xml
# t.me/TheVenomXD application/calendar+json
# t.me/TheVenomXD application/calendar+xml
# t.me/TheVenomXD application/call-completion
# t.me/TheVenomXD application/cals-1840
# t.me/TheVenomXD application/cbor
# t.me/TheVenomXD application/ccmp+xml
application/ccxml+xml				ccxml
# t.me/TheVenomXD application/cdfx+xml
application/cdmi-capability			cdmia
application/cdmi-container			cdmic
application/cdmi-domain				cdmid
application/cdmi-object				cdmio
application/cdmi-queue				cdmiq
# t.me/TheVenomXD application/cdni
# t.me/TheVenomXD application/cea
# t.me/TheVenomXD application/cea-2018+xml
# t.me/TheVenomXD application/cellml+xml
# t.me/TheVenomXD application/cfw
# t.me/TheVenomXD application/cms
# t.me/TheVenomXD application/cnrp+xml
# t.me/TheVenomXD application/coap-group+json
# t.me/TheVenomXD application/commonground
# t.me/TheVenomXD application/conference-info+xml
# t.me/TheVenomXD application/cpl+xml
# t.me/TheVenomXD application/csrattrs
# t.me/TheVenomXD application/csta+xml
# t.me/TheVenomXD application/cstadata+xml
# t.me/TheVenomXD application/csvm+json
application/cu-seeme				cu
# t.me/TheVenomXD application/cybercash
# t.me/TheVenomXD application/dash+xml
# t.me/TheVenomXD application/dashdelta
application/davmount+xml			davmount
# t.me/TheVenomXD application/dca-rft
# t.me/TheVenomXD application/dcd
# t.me/TheVenomXD application/dec-dx
# t.me/TheVenomXD application/dialog-info+xml
# t.me/TheVenomXD application/dicom
# t.me/TheVenomXD application/dii
# t.me/TheVenomXD application/dit
# t.me/TheVenomXD application/dns
application/docbook+xml				dbk
# t.me/TheVenomXD application/dskpp+xml
application/dssc+der				dssc
application/dssc+xml				xdssc
# t.me/TheVenomXD application/dvcs
application/ecmascript				ecma
# t.me/TheVenomXD application/edi-consent
# t.me/TheVenomXD application/edi-x12
# t.me/TheVenomXD application/edifact
# t.me/TheVenomXD application/efi
# t.me/TheVenomXD application/emergencycalldata.comment+xml
# t.me/TheVenomXD application/emergencycalldata.deviceinfo+xml
# t.me/TheVenomXD application/emergencycalldata.providerinfo+xml
# t.me/TheVenomXD application/emergencycalldata.serviceinfo+xml
# t.me/TheVenomXD application/emergencycalldata.subscriberinfo+xml
application/emma+xml				emma
# t.me/TheVenomXD application/emotionml+xml
# t.me/TheVenomXD application/encaprtp
# t.me/TheVenomXD application/epp+xml
application/epub+zip				epub
# t.me/TheVenomXD application/eshop
# t.me/TheVenomXD application/example
application/exi					exi
# t.me/TheVenomXD application/fastinfoset
# t.me/TheVenomXD application/fastsoap
# t.me/TheVenomXD application/fdt+xml
# t.me/TheVenomXD application/fits
application/font-tdpfr				pfr
# t.me/TheVenomXD application/framework-attributes+xml
# t.me/TheVenomXD application/geo+json
application/gml+xml				gml
application/gpx+xml				gpx
application/gxf					gxf
# t.me/TheVenomXD application/gzip
# t.me/TheVenomXD application/h224
# t.me/TheVenomXD application/held+xml
# t.me/TheVenomXD application/http
application/hyperstudio				stk
# t.me/TheVenomXD application/ibe-key-request+xml
# t.me/TheVenomXD application/ibe-pkg-reply+xml
# t.me/TheVenomXD application/ibe-pp-data
# t.me/TheVenomXD application/iges
# t.me/TheVenomXD application/im-iscomposing+xml
# t.me/TheVenomXD application/index
# t.me/TheVenomXD application/index.cmd
# t.me/TheVenomXD application/index.obj
# t.me/TheVenomXD application/index.response
# t.me/TheVenomXD application/index.vnd
application/inkml+xml				ink inkml
# t.me/TheVenomXD application/iotp
application/ipfix				ipfix
# t.me/TheVenomXD application/ipp
# t.me/TheVenomXD application/isup
# t.me/TheVenomXD application/its+xml
application/java-archive			jar
application/java-serialized-object		ser
application/java-vm				class
application/javascript				js
# t.me/TheVenomXD application/jose
# t.me/TheVenomXD application/jose+json
# t.me/TheVenomXD application/jrd+json
application/json				json
# t.me/TheVenomXD application/json-patch+json
# t.me/TheVenomXD application/json-seq
application/jsonml+json				jsonml
# t.me/TheVenomXD application/jwk+json
# t.me/TheVenomXD application/jwk-set+json
# t.me/TheVenomXD application/jwt
# t.me/TheVenomXD application/kpml-request+xml
# t.me/TheVenomXD application/kpml-response+xml
# t.me/TheVenomXD application/ld+json
# t.me/TheVenomXD application/lgr+xml
# t.me/TheVenomXD application/link-format
# t.me/TheVenomXD application/load-control+xml
application/lost+xml				lostxml
# t.me/TheVenomXD application/lostsync+xml
# t.me/TheVenomXD application/lxf
application/mac-binhex40			hqx
application/mac-compactpro			cpt
# t.me/TheVenomXD application/macwriteii
application/mads+xml				mads
application/marc				mrc
application/marcxml+xml				mrcx
application/mathematica				ma nb mb
application/mathml+xml				mathml
# t.me/TheVenomXD application/mathml-content+xml
# t.me/TheVenomXD application/mathml-presentation+xml
# t.me/TheVenomXD application/mbms-associated-procedure-description+xml
# t.me/TheVenomXD application/mbms-deregister+xml
# t.me/TheVenomXD application/mbms-envelope+xml
# t.me/TheVenomXD application/mbms-msk+xml
# t.me/TheVenomXD application/mbms-msk-response+xml
# t.me/TheVenomXD application/mbms-protection-description+xml
# t.me/TheVenomXD application/mbms-reception-report+xml
# t.me/TheVenomXD application/mbms-register+xml
# t.me/TheVenomXD application/mbms-register-response+xml
# t.me/TheVenomXD application/mbms-schedule+xml
# t.me/TheVenomXD application/mbms-user-service-description+xml
application/mbox				mbox
# t.me/TheVenomXD application/media-policy-dataset+xml
# t.me/TheVenomXD application/media_control+xml
application/mediaservercontrol+xml		mscml
# t.me/TheVenomXD application/merge-patch+json
application/metalink+xml			metalink
application/metalink4+xml			meta4
application/mets+xml				mets
# t.me/TheVenomXD application/mf4
# t.me/TheVenomXD application/mikey
application/mods+xml				mods
# t.me/TheVenomXD application/moss-keys
# t.me/TheVenomXD application/moss-signature
# t.me/TheVenomXD application/mosskey-data
# t.me/TheVenomXD application/mosskey-request
application/mp21				m21 mp21
application/mp4					mp4s
# t.me/TheVenomXD application/mpeg4-generic
# t.me/TheVenomXD application/mpeg4-iod
# t.me/TheVenomXD application/mpeg4-iod-xmt
# t.me/TheVenomXD application/mrb-consumer+xml
# t.me/TheVenomXD application/mrb-publish+xml
# t.me/TheVenomXD application/msc-ivr+xml
# t.me/TheVenomXD application/msc-mixer+xml
application/msword				doc dot
application/mxf					mxf
# t.me/TheVenomXD application/nasdata
# t.me/TheVenomXD application/news-checkgroups
# t.me/TheVenomXD application/news-groupinfo
# t.me/TheVenomXD application/news-transmission
# t.me/TheVenomXD application/nlsml+xml
# t.me/TheVenomXD application/nss
# t.me/TheVenomXD application/ocsp-request
# t.me/TheVenomXD application/ocsp-response
application/octet-stream	bin dms lrf mar so dist distz pkg bpk dump elc deploy
application/oda					oda
# t.me/TheVenomXD application/odx
application/oebps-package+xml			opf
application/ogg					ogx
application/omdoc+xml				omdoc
application/onenote				onetoc onetoc2 onetmp onepkg
application/oxps				oxps
# t.me/TheVenomXD application/p2p-overlay+xml
# t.me/TheVenomXD application/parityfec
application/patch-ops-error+xml			xer
application/pdf					pdf
# t.me/TheVenomXD application/pdx
application/pgp-encrypted			pgp
# t.me/TheVenomXD application/pgp-keys
application/pgp-signature			asc sig
application/pics-rules				prf
# t.me/TheVenomXD application/pidf+xml
# t.me/TheVenomXD application/pidf-diff+xml
application/pkcs10				p10
# t.me/TheVenomXD application/pkcs12
application/pkcs7-mime				p7m p7c
application/pkcs7-signature			p7s
application/pkcs8				p8
application/pkix-attr-cert			ac
application/pkix-cert				cer
application/pkix-crl				crl
application/pkix-pkipath			pkipath
application/pkixcmp				pki
application/pls+xml				pls
# t.me/TheVenomXD application/poc-settings+xml
application/postscript				ai eps ps
# t.me/TheVenomXD application/ppsp-tracker+json
# t.me/TheVenomXD application/problem+json
# t.me/TheVenomXD application/problem+xml
# t.me/TheVenomXD application/provenance+xml
# t.me/TheVenomXD application/prs.alvestrand.titrax-sheet
application/prs.cww				cww
# t.me/TheVenomXD application/prs.hpub+zip
# t.me/TheVenomXD application/prs.nprend
# t.me/TheVenomXD application/prs.plucker
# t.me/TheVenomXD application/prs.rdf-xml-crypt
# t.me/TheVenomXD application/prs.xsf+xml
application/pskc+xml				pskcxml
# t.me/TheVenomXD application/qsig
# t.me/TheVenomXD application/raptorfec
# t.me/TheVenomXD application/rdap+json
application/rdf+xml				rdf
application/reginfo+xml				rif
application/relax-ng-compact-syntax		rnc
# t.me/TheVenomXD application/remote-printing
# t.me/TheVenomXD application/reputon+json
application/resource-lists+xml			rl
application/resource-lists-diff+xml		rld
# t.me/TheVenomXD application/rfc+xml
# t.me/TheVenomXD application/riscos
# t.me/TheVenomXD application/rlmi+xml
application/rls-services+xml			rs
application/rpki-ghostbusters			gbr
application/rpki-manifest			mft
application/rpki-roa				roa
# t.me/TheVenomXD application/rpki-updown
application/rsd+xml				rsd
application/rss+xml				rss
application/rtf					rtf
# t.me/TheVenomXD application/rtploopback
# t.me/TheVenomXD application/rtx
# t.me/TheVenomXD application/samlassertion+xml
# t.me/TheVenomXD application/samlmetadata+xml
application/sbml+xml				sbml
# t.me/TheVenomXD application/scaip+xml
# t.me/TheVenomXD application/scim+json
application/scvp-cv-request			scq
application/scvp-cv-response			scs
application/scvp-vp-request			spq
application/scvp-vp-response			spp
application/sdp					sdp
# t.me/TheVenomXD application/sep+xml
# t.me/TheVenomXD application/sep-exi
# t.me/TheVenomXD application/session-info
# t.me/TheVenomXD application/set-payment
application/set-payment-initiation		setpay
# t.me/TheVenomXD application/set-registration
application/set-registration-initiation		setreg
# t.me/TheVenomXD application/sgml
# t.me/TheVenomXD application/sgml-open-catalog
application/shf+xml				shf
# t.me/TheVenomXD application/sieve
# t.me/TheVenomXD application/simple-Flow+xml
# t.me/TheVenomXD application/simple-message-summary
# t.me/TheVenomXD application/simplesymbolcontainer
# t.me/TheVenomXD application/slate
# t.me/TheVenomXD application/smil
application/smil+xml				smi smil
# t.me/TheVenomXD application/smpte336m
# t.me/TheVenomXD application/soap+fastinfoset
# t.me/TheVenomXD application/soap+xml
application/sparql-query			rq
application/sparql-results+xml			srx
# t.me/TheVenomXD application/spirits-event+xml
# t.me/TheVenomXD application/sql
application/srgs				gram
application/srgs+xml				grxml
application/sru+xml				sru
application/ssdl+xml				ssdl
application/ssml+xml				ssml
# t.me/TheVenomXD application/tamp-apex-update
# t.me/TheVenomXD application/tamp-apex-update-confirm
# t.me/TheVenomXD application/tamp-community-update
# t.me/TheVenomXD application/tamp-community-update-confirm
# t.me/TheVenomXD application/tamp-error
# t.me/TheVenomXD application/tamp-sequence-adjust
# t.me/TheVenomXD application/tamp-sequence-adjust-confirm
# t.me/TheVenomXD application/tamp-status-query
# t.me/TheVenomXD application/tamp-status-response
# t.me/TheVenomXD application/tamp-update
# t.me/TheVenomXD application/tamp-update-confirm
application/tei+xml				tei teicorpus
application/thraud+xml				tfi
# t.me/TheVenomXD application/timestamp-query
# t.me/TheVenomXD application/timestamp-reply
application/timestamped-data			tsd
# t.me/TheVenomXD application/ttml+xml
# t.me/TheVenomXD application/tve-trigger
# t.me/TheVenomXD application/ulpfec
# t.me/TheVenomXD application/urc-grpsheet+xml
# t.me/TheVenomXD application/urc-ressheet+xml
# t.me/TheVenomXD application/urc-tarExtractdesc+xml
# t.me/TheVenomXD application/urc-uisocketdesc+xml
# t.me/TheVenomXD application/vcard+json
# t.me/TheVenomXD application/vcard+xml
# t.me/TheVenomXD application/vemmi
# t.me/TheVenomXD application/vividence.scriptfile
# t.me/TheVenomXD application/vnd.3gpp-prose+xml
# t.me/TheVenomXD application/vnd.3gpp-prose-pc3ch+xml
# t.me/TheVenomXD application/vnd.3gpp.access-transfer-events+xml
# t.me/TheVenomXD application/vnd.3gpp.bsf+xml
# t.me/TheVenomXD application/vnd.3gpp.mid-call+xml
application/vnd.3gpp.pic-bw-large		plb
application/vnd.3gpp.pic-bw-small		psb
application/vnd.3gpp.pic-bw-var			pvb
# t.me/TheVenomXD application/vnd.3gpp.sms
# t.me/TheVenomXD application/vnd.3gpp.sms+xml
# t.me/TheVenomXD application/vnd.3gpp.srvcc-ext+xml
# t.me/TheVenomXD application/vnd.3gpp.srvcc-info+xml
# t.me/TheVenomXD application/vnd.3gpp.state-and-event-info+xml
# t.me/TheVenomXD application/vnd.3gpp.ussd+xml
# t.me/TheVenomXD application/vnd.3gpp2.bcmcsinfo+xml
# t.me/TheVenomXD application/vnd.3gpp2.sms
application/vnd.3gpp2.tcap			tcap
# t.me/TheVenomXD application/vnd.3lightssoftware.imagescal
application/vnd.3m.post-it-notes		pwn
application/vnd.accpac.simply.aso		aso
application/vnd.accpac.simply.imp		imp
application/vnd.acucobol			acu
application/vnd.acucorp				atc acutc
application/vnd.adobe.air-application-installer-package+zip	air
# t.me/TheVenomXD application/vnd.adobe.flash.movie
application/vnd.adobe.formscentral.fcdt		fcdt
application/vnd.adobe.fxp			fxp fxpl
# t.me/TheVenomXD application/vnd.adobe.partial-upload
application/vnd.adobe.xdp+xml			xdp
application/vnd.adobe.xfdf			xfdf
# t.me/TheVenomXD application/vnd.aether.imp
# t.me/TheVenomXD application/vnd.ah-barcode
application/vnd.ahead.space			ahead
application/vnd.airzip.filesecure.azf		azf
application/vnd.airzip.filesecure.azs		azs
application/vnd.amazon.ebook			azw
# t.me/TheVenomXD application/vnd.amazon.mobi8-ebook
application/vnd.americandynamics.acc		acc
application/vnd.amiga.ami			ami
# t.me/TheVenomXD application/vnd.amundsen.maze+xml
application/vnd.android.package-archive		apk
# t.me/TheVenomXD application/vnd.anki
application/vnd.anser-web-certificate-issue-initiation	cii
application/vnd.anser-web-funds-transfer-initiation	fti
application/vnd.antix.game-component		atx
# t.me/TheVenomXD application/vnd.apache.thrift.binary
# t.me/TheVenomXD application/vnd.apache.thrift.compact
# t.me/TheVenomXD application/vnd.apache.thrift.json
# t.me/TheVenomXD application/vnd.Ai+json
application/vnd.apple.installer+xml		mpkg
application/vnd.apple.mpegurl			m3u8
# t.me/TheVenomXD application/vnd.arastra.swi
application/vnd.aristanetworks.swi		swi
# t.me/TheVenomXD application/vnd.artsquare
application/vnd.astraea-software.iota		iota
application/vnd.audiograph			aep
# t.me/TheVenomXD application/vnd.autopackage
# t.me/TheVenomXD application/vnd.avistar+xml
# t.me/TheVenomXD application/vnd.balsamiq.bmml+xml
# t.me/TheVenomXD application/vnd.balsamiq.bmpr
# t.me/TheVenomXD application/vnd.bekitzur-stech+json
# t.me/TheVenomXD application/vnd.biopax.rdf+xml
application/vnd.blueice.multipass		mpm
# t.me/TheVenomXD application/vnd.bluetooth.ep.oob
# t.me/TheVenomXD application/vnd.bluetooth.le.oob
application/vnd.bmi				bmi
application/vnd.businessobjects			rep
# t.me/TheVenomXD application/vnd.cab-jscript
# t.me/TheVenomXD application/vnd.canon-cpdl
# t.me/TheVenomXD application/vnd.canon-lips
# t.me/TheVenomXD application/vnd.cendio.thinlinc.clientconf
# t.me/TheVenomXD application/vnd.century-systems.tcp_stream
application/vnd.chemdraw+xml			cdxml
# t.me/TheVenomXD application/vnd.chess-pgn
application/vnd.chipnuts.karaoke-mmd		mmd
application/vnd.cinderella			cdy
# t.me/TheVenomXD application/vnd.cirpack.isdn-ext
# t.me/TheVenomXD application/vnd.citationstyles.style+xml
application/vnd.claymore			cla
application/vnd.cloanto.rp9			rp9
application/vnd.clonk.c4group			c4g c4d c4f c4p c4u
application/vnd.cluetrust.cartomobile-config		c11amc
application/vnd.cluetrust.cartomobile-config-pkg	c11amz
# t.me/TheVenomXD application/vnd.coffeescript
# t.me/TheVenomXD application/vnd.collection+json
# t.me/TheVenomXD application/vnd.collection.doc+json
# t.me/TheVenomXD application/vnd.collection.next+json
# t.me/TheVenomXD application/vnd.comicbook+zip
# t.me/TheVenomXD application/vnd.commerce-battelle
application/vnd.commonspace			csp
application/vnd.contact.cmsg			cdbcmsg
# t.me/TheVenomXD application/vnd.coreos.ignition+json
application/vnd.cosmocaller			cmc
application/vnd.crick.clicker			clkx
application/vnd.crick.clicker.keyboard		clkk
application/vnd.crick.clicker.palette		clkp
application/vnd.crick.clicker.template		clkt
application/vnd.crick.clicker.wordbank		clkw
application/vnd.criticaltools.wbs+xml		wbs
application/vnd.ctc-posml			pml
# t.me/TheVenomXD application/vnd.ctct.ws+xml
# t.me/TheVenomXD application/vnd.cups-pdf
# t.me/TheVenomXD application/vnd.cups-postscript
application/vnd.cups-ppd			ppd
# t.me/TheVenomXD application/vnd.cups-raster
# t.me/TheVenomXD application/vnd.cups-raw
# t.me/TheVenomXD application/vnd.curl
application/vnd.curl.car			car
application/vnd.curl.pcurl			pcurl
# t.me/TheVenomXD application/vnd.cyan.dean.root+xml
# t.me/TheVenomXD application/vnd.cybank
application/vnd.dart				dart
application/vnd.data-vision.rdz			rdz
# t.me/TheVenomXD application/vnd.debian.binary-package
application/vnd.dece.data			uvf uvvf uvd uvvd
application/vnd.dece.ttml+xml			uvt uvvt
application/vnd.dece.unspecified		uvx uvvx
application/vnd.dece.zip			uvz uvvz
application/vnd.denovo.fcselayout-link		fe_launch
# t.me/TheVenomXD application/vnd.desmume.movie
# t.me/TheVenomXD application/vnd.dir-bi.plate-dl-nosuffix
# t.me/TheVenomXD application/vnd.dm.delegation+xml
application/vnd.dna				dna
# t.me/TheVenomXD application/vnd.document+json
application/vnd.dolby.mlp			mlp
# t.me/TheVenomXD application/vnd.dolby.mobile.1
# t.me/TheVenomXD application/vnd.dolby.mobile.2
# t.me/TheVenomXD application/vnd.doremir.scorecloud-binary-document
application/vnd.dpgraph				dpg
application/vnd.dreamfactory			dfac
# t.me/TheVenomXD application/vnd.drive+json
application/vnd.ds-keypoint			kpxx
# t.me/TheVenomXD application/vnd.dtg.local
# t.me/TheVenomXD application/vnd.dtg.local.flash
# t.me/TheVenomXD application/vnd.dtg.local.html
application/vnd.dvb.ait				ait
# t.me/TheVenomXD application/vnd.dvb.dvbj
# t.me/TheVenomXD application/vnd.dvb.esgcontainer
# t.me/TheVenomXD application/vnd.dvb.ipdcdftnotifaccess
# t.me/TheVenomXD application/vnd.dvb.ipdcesgaccess
# t.me/TheVenomXD application/vnd.dvb.ipdcesgaccess2
# t.me/TheVenomXD application/vnd.dvb.ipdcesgpdd
# t.me/TheVenomXD application/vnd.dvb.ipdcroaming
# t.me/TheVenomXD application/vnd.dvb.iptv.alfec-base
# t.me/TheVenomXD application/vnd.dvb.iptv.alfec-enhancement
# t.me/TheVenomXD application/vnd.dvb.notif-aggregate-root+xml
# t.me/TheVenomXD application/vnd.dvb.notif-container+xml
# t.me/TheVenomXD application/vnd.dvb.notif-generic+xml
# t.me/TheVenomXD application/vnd.dvb.notif-ia-msglist+xml
# t.me/TheVenomXD application/vnd.dvb.notif-ia-registration-request+xml
# t.me/TheVenomXD application/vnd.dvb.notif-ia-registration-response+xml
# t.me/TheVenomXD application/vnd.dvb.notif-init+xml
# t.me/TheVenomXD application/vnd.dvb.pfr
application/vnd.dvb.service			svc
# t.me/TheVenomXD application/vnd.dxr
application/vnd.dynageo				geo
# t.me/TheVenomXD application/vnd.dzr
# t.me/TheVenomXD application/vnd.easykaraoke.cdgdownload
# t.me/TheVenomXD application/vnd.ecdis-update
application/vnd.ecowin.chart			mag
# t.me/TheVenomXD application/vnd.ecowin.filerequest
# t.me/TheVenomXD application/vnd.ecowin.fileupdate
# t.me/TheVenomXD application/vnd.ecowin.series
# t.me/TheVenomXD application/vnd.ecowin.seriesrequest
# t.me/TheVenomXD application/vnd.ecowin.seriesupdate
# t.me/TheVenomXD application/vnd.emclient.accessrequest+xml
application/vnd.enliven				nml
# t.me/TheVenomXD application/vnd.enphase.envoy
# t.me/TheVenomXD application/vnd.eprints.data+xml
application/vnd.epson.esf			esf
application/vnd.epson.msf			msf
application/vnd.epson.quickanime		qam
application/vnd.epson.salt			slt
application/vnd.epson.ssf			ssf
# t.me/TheVenomXD application/vnd.ericsson.quickcall
application/vnd.eszigno3+xml			es3 et3
# t.me/TheVenomXD application/vnd.etsi.aoc+xml
# t.me/TheVenomXD application/vnd.etsi.asic-e+zip
# t.me/TheVenomXD application/vnd.etsi.asic-s+zip
# t.me/TheVenomXD application/vnd.etsi.cug+xml
# t.me/TheVenomXD application/vnd.etsi.iptvcommand+xml
# t.me/TheVenomXD application/vnd.etsi.iptvdiscovery+xml
# t.me/TheVenomXD application/vnd.etsi.iptvprofile+xml
# t.me/TheVenomXD application/vnd.etsi.iptvsad-bc+xml
# t.me/TheVenomXD application/vnd.etsi.iptvsad-cod+xml
# t.me/TheVenomXD application/vnd.etsi.iptvsad-npvr+xml
# t.me/TheVenomXD application/vnd.etsi.iptvservice+xml
# t.me/TheVenomXD application/vnd.etsi.iptvsync+xml
# t.me/TheVenomXD application/vnd.etsi.iptvueprofile+xml
# t.me/TheVenomXD application/vnd.etsi.mcid+xml
# t.me/TheVenomXD application/vnd.etsi.mheg5
# t.me/TheVenomXD application/vnd.etsi.overload-control-policy-dataset+xml
# t.me/TheVenomXD application/vnd.etsi.pstn+xml
# t.me/TheVenomXD application/vnd.etsi.sci+xml
# t.me/TheVenomXD application/vnd.etsi.simservs+xml
# t.me/TheVenomXD application/vnd.etsi.timestamp-token
# t.me/TheVenomXD application/vnd.etsi.tsl+xml
# t.me/TheVenomXD application/vnd.etsi.tsl.der
# t.me/TheVenomXD application/vnd.eudora.data
application/vnd.ezpix-album			ez2
application/vnd.ezpix-package			ez3
# t.me/TheVenomXD application/vnd.f-secure.mobile
# t.me/TheVenomXD application/vnd.fastcopy-disk-image
application/vnd.fdf				fdf
application/vnd.fdsn.mseed			mseed
application/vnd.fdsn.seed			seed dataless
# t.me/TheVenomXD application/vnd.ffsns
# t.me/TheVenomXD application/vnd.filmit.zfc
# t.me/TheVenomXD application/vnd.fints
# t.me/TheVenomXD application/vnd.firemonkeys.cloudcell
application/vnd.flographit			gph
application/vnd.fluxtime.clip			ftc
# t.me/TheVenomXD application/vnd.font-fontforge-sfd
application/vnd.framemaker			fm frame maker book
application/vnd.frogans.fnc			fnc
application/vnd.frogans.ltf			ltf
application/vnd.fsc.weblaunch			fsc
application/vnd.fujitsu.oasys			oas
application/vnd.fujitsu.oasys2			oa2
application/vnd.fujitsu.oasys3			oa3
application/vnd.fujitsu.oasysgp			fg5
application/vnd.fujitsu.oasysprs		bh2
# t.me/TheVenomXD application/vnd.fujixerox.art-ex
# t.me/TheVenomXD application/vnd.fujixerox.art4
application/vnd.fujixerox.ddd			ddd
application/vnd.fujixerox.docuworks		xdw
application/vnd.fujixerox.docuworks.binder	xbd
# t.me/TheVenomXD application/vnd.fujixerox.docuworks.container
# t.me/TheVenomXD application/vnd.fujixerox.hbpl
# t.me/TheVenomXD application/vnd.fut-misnet
application/vnd.fuzzysheet			fzs
application/vnd.genomatix.tuxedo		txd
# t.me/TheVenomXD application/vnd.geo+json
# t.me/TheVenomXD application/vnd.geocube+xml
application/vnd.geogebra.file			ggb
application/vnd.geogebra.tool			ggt
application/vnd.geometry-explorer		gex gre
application/vnd.geonext				gxt
application/vnd.geoplan				g2w
application/vnd.geospace			g3w
# t.me/TheVenomXD application/vnd.gerber
# t.me/TheVenomXD application/vnd.globalplatform.card-content-mgt
# t.me/TheVenomXD application/vnd.globalplatform.card-content-mgt-response
application/vnd.gmx				gmx
application/vnd.google-earth.kml+xml		kml
application/vnd.google-earth.kmz		kmz
# t.me/TheVenomXD application/vnd.gov.sk.e-form+xml
# t.me/TheVenomXD application/vnd.gov.sk.e-form+zip
# t.me/TheVenomXD application/vnd.gov.sk.xmldatacontainer+xml
application/vnd.grafeq				gqf gqs
# t.me/TheVenomXD application/vnd.gridmp
application/vnd.groove-account			gac
application/vnd.groove-help			ghf
application/vnd.groove-identity-message		gim
application/vnd.groove-injector			grv
application/vnd.groove-tool-message		gtm
application/vnd.groove-tool-template		tpl
application/vnd.groove-vcard			vcg
# t.me/TheVenomXD application/vnd.hal+json
application/vnd.hal+xml				hal
application/vnd.handheld-entertainment+xml	zmm
application/vnd.hbci				hbci
# t.me/TheVenomXD application/vnd.hcl-bireports
# t.me/TheVenomXD application/vnd.hdt
# t.me/TheVenomXD application/vnd.heroku+json
application/vnd.hhe.lesson-player		les
application/vnd.hp-hpgl				hpgl
application/vnd.hp-hpid				hpid
application/vnd.hp-hps				hps
application/vnd.hp-jlyt				jlt
application/vnd.hp-pcl				pcl
application/vnd.hp-pclxl			pclxl
# t.me/TheVenomXD application/vnd.httphone
application/vnd.hydrostatix.sof-data		sfd-hdstx
# t.me/TheVenomXD application/vnd.hyperdrive+json
# t.me/TheVenomXD application/vnd.hzn-3d-crossword
# t.me/TheVenomXD application/vnd.ibm.afplinedata
# t.me/TheVenomXD application/vnd.ibm.electronic-media
application/vnd.ibm.minipay			mpy
application/vnd.ibm.modcap			afp listafp list3820
application/vnd.ibm.rights-management		irm
application/vnd.ibm.secure-container		sc
application/vnd.iccprofile			icc icm
# t.me/TheVenomXD application/vnd.ieee.1905
application/vnd.igloader			igl
application/vnd.immervision-ivp			ivp
application/vnd.immervision-ivu			ivu
# t.me/TheVenomXD application/vnd.ims.imsccv1p1
# t.me/TheVenomXD application/vnd.ims.imsccv1p2
# t.me/TheVenomXD application/vnd.ims.imsccv1p3
# t.me/TheVenomXD application/vnd.ims.lis.v2.result+json
# t.me/TheVenomXD application/vnd.ims.lti.v2.toolconsumerprofile+json
# t.me/TheVenomXD application/vnd.ims.lti.v2.toolproxy+json
# t.me/TheVenomXD application/vnd.ims.lti.v2.toolproxy.id+json
# t.me/TheVenomXD application/vnd.ims.lti.v2.toolsettings+json
# t.me/TheVenomXD application/vnd.ims.lti.v2.toolsettings.simple+json
# t.me/TheVenomXD application/vnd.informedcontrol.rms+xml
# t.me/TheVenomXD application/vnd.informix-visionary
# t.me/TheVenomXD application/vnd.infotech.project
# t.me/TheVenomXD application/vnd.infotech.project+xml
# t.me/TheVenomXD application/vnd.innopath.wamp.notification
application/vnd.insors.igm			igm
application/vnd.intercon.formnet		xpw xpx
application/vnd.intergeo			i2g
# t.me/TheVenomXD application/vnd.intertrust.digibox
# t.me/TheVenomXD application/vnd.intertrust.nncp
application/vnd.intu.qbo			qbo
application/vnd.intu.qfx			qfx
# t.me/TheVenomXD application/vnd.iptc.g2.catalogitem+xml
# t.me/TheVenomXD application/vnd.iptc.g2.conceptitem+xml
# t.me/TheVenomXD application/vnd.iptc.g2.knowledgeitem+xml
# t.me/TheVenomXD application/vnd.iptc.g2.newsitem+xml
# t.me/TheVenomXD application/vnd.iptc.g2.newsmessage+xml
# t.me/TheVenomXD application/vnd.iptc.g2.packageitem+xml
# t.me/TheVenomXD application/vnd.iptc.g2.planningitem+xml
application/vnd.ipunplugged.rcprofile		rcprofile
application/vnd.irepository.package+xml		irp
application/vnd.is-xpr				xpr
application/vnd.isac.fcs			fcs
application/vnd.jam				jam
# t.me/TheVenomXD application/vnd.japannet-directory-service
# t.me/TheVenomXD application/vnd.japannet-jpnstore-wakeup
# t.me/TheVenomXD application/vnd.japannet-payment-wakeup
# t.me/TheVenomXD application/vnd.japannet-registration
# t.me/TheVenomXD application/vnd.japannet-registration-wakeup
# t.me/TheVenomXD application/vnd.japannet-setstore-wakeup
# t.me/TheVenomXD application/vnd.japannet-verification
# t.me/TheVenomXD application/vnd.japannet-verification-wakeup
application/vnd.jcp.javame.midlet-rms		rms
application/vnd.jisp				jisp
application/vnd.joost.joda-archive		joda
# t.me/TheVenomXD application/vnd.jsk.isdn-ngn
application/vnd.kahootz				ktz ktr
application/vnd.kde.karbon			karbon
application/vnd.kde.kchart			chrt
application/vnd.kde.kformula			kfo
application/vnd.kde.kivio			flw
application/vnd.kde.kontour			kon
application/vnd.kde.kpresenter			kpr kpt
application/vnd.kde.kspread			ksp
application/vnd.kde.kword			kwd kwt
application/vnd.kenameaapp			htke
application/vnd.kidspiration			kia
application/vnd.kinar				kne knp
application/vnd.koan				skp skd skt skm
application/vnd.kodak-descriptor		sse
application/vnd.las.las+xml			lasxml
# t.me/TheVenomXD application/vnd.liberty-request+xml
application/vnd.llamagraphics.life-balance.desktop	lbd
application/vnd.llamagraphics.life-balance.exchange+xml	lbe
application/vnd.lotus-1-2-3			123
application/vnd.lotus-approach			apr
application/vnd.lotus-freelance			pre
application/vnd.lotus-notes			nsf
application/vnd.lotus-organizer			org
application/vnd.lotus-screencam			scm
application/vnd.lotus-wordpro			lwp
application/vnd.macports.portpkg		portpkg
# t.me/TheVenomXD application/vnd.mapbox-vector-tile
# t.me/TheVenomXD application/vnd.marlin.drm.actiontoken+xml
# t.me/TheVenomXD application/vnd.marlin.drm.conftoken+xml
# t.me/TheVenomXD application/vnd.marlin.drm.license+xml
# t.me/TheVenomXD application/vnd.marlin.drm.mdcf
# t.me/TheVenomXD application/vnd.mason+json
# t.me/TheVenomXD application/vnd.maxmind.maxmind-db
application/vnd.mcd				mcd
application/vnd.medcalcdata			mc1
application/vnd.mediastation.cdkey		cdkey
# t.me/TheVenomXD application/vnd.meridian-slingshot
application/vnd.mfer				mwf
application/vnd.mfmp				mfm
# t.me/TheVenomXD application/vnd.micro+json
application/vnd.micrografx.flo			flo
application/vnd.micrografx.igx			igx
# t.me/TheVenomXD application/vnd.microsoft.portable-executable
# t.me/TheVenomXD application/vnd.miele+json
application/vnd.mif				mif
# t.me/TheVenomXD application/vnd.minisoft-hp3000-save
# t.me/TheVenomXD application/vnd.mitsubishi.misty-guard.trustweb
application/vnd.mobius.daf			daf
application/vnd.mobius.dis			dis
application/vnd.mobius.mbk			mbk
application/vnd.mobius.mqy			mqy
application/vnd.mobius.msl			msl
application/vnd.mobius.plc			plc
application/vnd.mobius.txf			txf
application/vnd.mophun.application		mpn
application/vnd.mophun.certificate		mpc
# t.me/TheVenomXD application/vnd.motorola.flexsuite
# t.me/TheVenomXD application/vnd.motorola.flexsuite.adsi
# t.me/TheVenomXD application/vnd.motorola.flexsuite.fis
# t.me/TheVenomXD application/vnd.motorola.flexsuite.gotap
# t.me/TheVenomXD application/vnd.motorola.flexsuite.kmr
# t.me/TheVenomXD application/vnd.motorola.flexsuite.ttc
# t.me/TheVenomXD application/vnd.motorola.flexsuite.wem
# t.me/TheVenomXD application/vnd.motorola.iprm
application/vnd.mozilla.xul+xml			xul
# t.me/TheVenomXD application/vnd.ms-3mfdocument
application/vnd.ms-artgalry			cil
# t.me/TheVenomXD application/vnd.ms-asf
application/vnd.ms-cab-compressed		cab
# t.me/TheVenomXD application/vnd.ms-color.iccprofile
application/vnd.ms-excel			xls xlm xla xlc xlt xlw
application/vnd.ms-excel.addin.macroenabled.12		xlam
application/vnd.ms-excel.sheet.binary.macroenabled.12	xlsb
application/vnd.ms-excel.sheet.macroenabled.12		xlsm
application/vnd.ms-excel.template.macroenabled.12	xltm
application/vnd.ms-fontobject			eot
application/vnd.ms-htmlhelp			chm
application/vnd.ms-ims				ims
application/vnd.ms-lrm				lrm
# t.me/TheVenomXD application/vnd.ms-office.activex+xml
application/vnd.ms-officetheme			thmx
# t.me/TheVenomXD application/vnd.ms-opentype
# t.me/TheVenomXD application/vnd.ms-package.obfuscated-opentype
application/vnd.ms-pki.seccat			cat
application/vnd.ms-pki.stl			stl
# t.me/TheVenomXD application/vnd.ms-playready.initiator+xml
application/vnd.ms-powerpoint			ppt pps pot
application/vnd.ms-powerpoint.addin.macroenabled.12		ppam
application/vnd.ms-powerpoint.presentation.macroenabled.12	pptm
application/vnd.ms-powerpoint.slide.macroenabled.12		sldm
application/vnd.ms-powerpoint.slideshow.macroenabled.12		ppsm
application/vnd.ms-powerpoint.template.macroenabled.12		potm
# t.me/TheVenomXD application/vnd.ms-printdevicecapabilities+xml
# t.me/TheVenomXD application/vnd.ms-printing.printticket+xml
# t.me/TheVenomXD application/vnd.ms-printschematicket+xml
application/vnd.ms-project			mpp mpt
# t.me/TheVenomXD application/vnd.ms-tnef
# t.me/TheVenomXD application/vnd.ms-windows.devicepairing
# t.me/TheVenomXD application/vnd.ms-windows.nwprinting.oob
# t.me/TheVenomXD application/vnd.ms-windows.printerpairing
# t.me/TheVenomXD application/vnd.ms-windows.wsd.oob
# t.me/TheVenomXD application/vnd.ms-wmdrm.lic-chlg-req
# t.me/TheVenomXD application/vnd.ms-wmdrm.lic-resp
# t.me/TheVenomXD application/vnd.ms-wmdrm.meter-chlg-req
# t.me/TheVenomXD application/vnd.ms-wmdrm.meter-resp
application/vnd.ms-word.document.macroenabled.12	docm
application/vnd.ms-word.template.macroenabled.12	dotm
application/vnd.ms-works			wps wks wcm wdb
application/vnd.ms-wpl				wpl
application/vnd.ms-xpsdocument			xps
# t.me/TheVenomXD application/vnd.msa-disk-image
application/vnd.mseq				mseq
# t.me/TheVenomXD application/vnd.msign
# t.me/TheVenomXD application/vnd.multiad.creator
# t.me/TheVenomXD application/vnd.multiad.creator.cif
# t.me/TheVenomXD application/vnd.music-niff
application/vnd.musician			mus
application/vnd.muvee.style			msty
application/vnd.mynfc				taglet
# t.me/TheVenomXD application/vnd.ncd.control
# t.me/TheVenomXD application/vnd.ncd.reference
# t.me/TheVenomXD application/vnd.nervana
# t.me/TheVenomXD application/vnd.netfpx
application/vnd.neurolanguage.nlu		nlu
# t.me/TheVenomXD application/vnd.nintendo.nitro.rom
# t.me/TheVenomXD application/vnd.nintendo.snes.rom
application/vnd.nitf				ntf nitf
application/vnd.noblenet-directory		nnd
application/vnd.noblenet-sealer			nns
application/vnd.noblenet-web			nnw
# t.me/TheVenomXD application/vnd.nokia.catalogs
# t.me/TheVenomXD application/vnd.nokia.conml+wbxml
# t.me/TheVenomXD application/vnd.nokia.conml+xml
# t.me/TheVenomXD application/vnd.nokia.iptv.config+xml
# t.me/TheVenomXD application/vnd.nokia.isds-radio-presets
# t.me/TheVenomXD application/vnd.nokia.landmark+wbxml
# t.me/TheVenomXD application/vnd.nokia.landmark+xml
# t.me/TheVenomXD application/vnd.nokia.landmarkcollection+xml
# t.me/TheVenomXD application/vnd.nokia.n-gage.ac+xml
application/vnd.nokia.n-gage.data		ngdat
application/vnd.nokia.n-gage.symbian.install	n-gage
# t.me/TheVenomXD application/vnd.nokia.ncd
# t.me/TheVenomXD application/vnd.nokia.pcd+wbxml
# t.me/TheVenomXD application/vnd.nokia.pcd+xml
application/vnd.nokia.radio-preset		rpst
application/vnd.nokia.radio-presets		rpss
application/vnd.novadigm.edm			edm
application/vnd.novadigm.edx			edx
application/vnd.novadigm.ext			ext
# t.me/TheVenomXD application/vnd.ntt-local.content-share
# t.me/TheVenomXD application/vnd.ntt-local.file-transfer
# t.me/TheVenomXD application/vnd.ntt-local.ogw_remote-access
# t.me/TheVenomXD application/vnd.ntt-local.sip-ta_remote
# t.me/TheVenomXD application/vnd.ntt-local.sip-ta_tcp_stream
application/vnd.oasis.opendocument.chart		odc
application/vnd.oasis.opendocument.chart-template	otc
application/vnd.oasis.opendocument.database		odb
application/vnd.oasis.opendocument.formula		odf
application/vnd.oasis.opendocument.formula-template	odft
application/vnd.oasis.opendocument.graphics		odg
application/vnd.oasis.opendocument.graphics-template	otg
application/vnd.oasis.opendocument.image		odi
application/vnd.oasis.opendocument.image-template	oti
application/vnd.oasis.opendocument.presentation		odp
application/vnd.oasis.opendocument.presentation-template	otp
application/vnd.oasis.opendocument.spreadsheet		ods
application/vnd.oasis.opendocument.spreadsheet-template	ots
application/vnd.oasis.opendocument.text			odt
application/vnd.oasis.opendocument.text-master		odm
application/vnd.oasis.opendocument.text-template	ott
application/vnd.oasis.opendocument.text-web		oth
# t.me/TheVenomXD application/vnd.obn
# t.me/TheVenomXD application/vnd.oftn.l10n+json
# t.me/TheVenomXD application/vnd.oipf.contentaccessdownload+xml
# t.me/TheVenomXD application/vnd.oipf.contentaccessstreaming+xml
# t.me/TheVenomXD application/vnd.oipf.cspg-hexbinary
# t.me/TheVenomXD application/vnd.oipf.dae.svg+xml
# t.me/TheVenomXD application/vnd.oipf.dae.xhtml+xml
# t.me/TheVenomXD application/vnd.oipf.mippvcontrolmessage+xml
# t.me/TheVenomXD application/vnd.oipf.pae.gem
# t.me/TheVenomXD application/vnd.oipf.spdiscovery+xml
# t.me/TheVenomXD application/vnd.oipf.spdlist+xml
# t.me/TheVenomXD application/vnd.oipf.ueprofile+xml
# t.me/TheVenomXD application/vnd.oipf.userprofile+xml
application/vnd.olpc-sugar			xo
# t.me/TheVenomXD application/vnd.oma-scws-config
# t.me/TheVenomXD application/vnd.oma-scws-http-request
# t.me/TheVenomXD application/vnd.oma-scws-http-response
# t.me/TheVenomXD application/vnd.oma.bcast.associated-procedure-parameter+xml
# t.me/TheVenomXD application/vnd.oma.bcast.drm-trigger+xml
# t.me/TheVenomXD application/vnd.oma.bcast.imd+xml
# t.me/TheVenomXD application/vnd.oma.bcast.ltkm
# t.me/TheVenomXD application/vnd.oma.bcast.notification+xml
# t.me/TheVenomXD application/vnd.oma.bcast.provisioningtrigger
# t.me/TheVenomXD application/vnd.oma.bcast.sgboot
# t.me/TheVenomXD application/vnd.oma.bcast.sgdd+xml
# t.me/TheVenomXD application/vnd.oma.bcast.sgdu
# t.me/TheVenomXD application/vnd.oma.bcast.simple-symbol-container
# t.me/TheVenomXD application/vnd.oma.bcast.smartcard-trigger+xml
# t.me/TheVenomXD application/vnd.oma.bcast.sprov+xml
# t.me/TheVenomXD application/vnd.oma.bcast.stkm
# t.me/TheVenomXD application/vnd.oma.cab-address-book+xml
# t.me/TheVenomXD application/vnd.oma.cab-feature-handler+xml
# t.me/TheVenomXD application/vnd.oma.cab-pcc+xml
# t.me/TheVenomXD application/vnd.oma.cab-subs-invite+xml
# t.me/TheVenomXD application/vnd.oma.cab-user-prefs+xml
# t.me/TheVenomXD application/vnd.oma.dcd
# t.me/TheVenomXD application/vnd.oma.dcdc
application/vnd.oma.dd2+xml			dd2
# t.me/TheVenomXD application/vnd.oma.drm.risd+xml
# t.me/TheVenomXD application/vnd.oma.group-usage-list+xml
# t.me/TheVenomXD application/vnd.oma.lwm2m+json
# t.me/TheVenomXD application/vnd.oma.lwm2m+tlv
# t.me/TheVenomXD application/vnd.oma.pal+xml
# t.me/TheVenomXD application/vnd.oma.poc.detailed-progress-report+xml
# t.me/TheVenomXD application/vnd.oma.poc.final-report+xml
# t.me/TheVenomXD application/vnd.oma.poc.groups+xml
# t.me/TheVenomXD application/vnd.oma.poc.invocation-descriptor+xml
# t.me/TheVenomXD application/vnd.oma.poc.optimized-progress-report+xml
# t.me/TheVenomXD application/vnd.oma.push
# t.me/TheVenomXD application/vnd.oma.scidm.messages+xml
# t.me/TheVenomXD application/vnd.oma.xcap-directory+xml
# t.me/TheVenomXD application/vnd.omads-email+xml
# t.me/TheVenomXD application/vnd.omads-file+xml
# t.me/TheVenomXD application/vnd.omads-folder+xml
# t.me/TheVenomXD application/vnd.omaloc-supl-init
# t.me/TheVenomXD application/vnd.onepager
# t.me/TheVenomXD application/vnd.openblox.game+xml
# t.me/TheVenomXD application/vnd.openblox.game-binary
# t.me/TheVenomXD application/vnd.openeye.oeb
application/vnd.openofficeorg.extension		oxt
# t.me/TheVenomXD application/vnd.openxmlformats-officedocument.custom-properties+xml
# t.me/TheVenomXD application/vnd.openxmlformats-officedocument.customxmlproperties+xml
# t.me/TheVenomXD application/vnd.openxmlformats-officedocument.drawing+xml
# t.me/TheVenomXD application/vnd.openxmlformats-officedocument.drawingml.chart+xml
# t.me/TheVenomXD application/vnd.openxmlformats-officedocument.drawingml.chartshapes+xml
# t.me/TheVenomXD application/vnd.openxmlformats-officedocument.drawingml.diagramcolors+xml
# t.me/TheVenomXD application/vnd.openxmlformats-officedocument.drawingml.diagramdata+xml
# t.me/TheVenomXD application/vnd.openxmlformats-officedocument.drawingml.diagramlayout+xml
# t.me/TheVenomXD application/vnd.openxmlformats-officedocument.drawingml.diagramstyle+xml
# t.me/TheVenomXD application/vnd.openxmlformats-officedocument.extended-properties+xml
# t.me/TheVenomXD application/vnd.openxmlformats-officedocument.presentationml.commentauthors+xml
# t.me/TheVenomXD application/vnd.openxmlformats-officedocument.presentationml.comments+xml
# t.me/TheVenomXD application/vnd.openxmlformats-officedocument.presentationml.handoutmaster+xml
# t.me/TheVenomXD application/vnd.openxmlformats-officedocument.presentationml.notesmaster+xml
# t.me/TheVenomXD application/vnd.openxmlformats-officedocument.presentationml.notesslide+xml
application/vnd.openxmlformats-officedocument.presentationml.presentation	pptx
# t.me/TheVenomXD application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml
# t.me/TheVenomXD application/vnd.openxmlformats-officedocument.presentationml.presprops+xml
application/vnd.openxmlformats-officedocument.presentationml.slide	sldx
# t.me/TheVenomXD application/vnd.openxmlformats-officedocument.presentationml.slide+xml
# t.me/TheVenomXD application/vnd.openxmlformats-officedocument.presentationml.slidelayout+xml
# t.me/TheVenomXD application/vnd.openxmlformats-officedocument.presentationml.slidemaster+xml
application/vnd.openxmlformats-officedocument.presentationml.slideshow	ppsx
# t.me/TheVenomXD application/vnd.openxmlformats-officedocument.presentationml.slideshow.main+xml
# t.me/TheVenomXD application/vnd.openxmlformats-officedocument.presentationml.slideupdateinfo+xml
# t.me/TheVenomXD application/vnd.openxmlformats-officedocument.presentationml.tablestyles+xml
# t.me/TheVenomXD application/vnd.openxmlformats-officedocument.presentationml.tags+xml
application/vnd.openxmlformats-officedocument.presentationml.template	potx
# t.me/TheVenomXD application/vnd.openxmlformats-officedocument.presentationml.template.main+xml
# t.me/TheVenomXD application/vnd.openxmlformats-officedocument.presentationml.viewprops+xml
# t.me/TheVenomXD application/vnd.openxmlformats-officedocument.spreadsheetml.calcchain+xml
# t.me/TheVenomXD application/vnd.openxmlformats-officedocument.spreadsheetml.chartsheet+xml
# t.me/TheVenomXD application/vnd.openxmlformats-officedocument.spreadsheetml.comments+xml
# t.me/TheVenomXD application/vnd.openxmlformats-officedocument.spreadsheetml.connections+xml
# t.me/TheVenomXD application/vnd.openxmlformats-officedocument.spreadsheetml.dialogsheet+xml
# t.me/TheVenomXD application/vnd.openxmlformats-officedocument.spreadsheetml.externallink+xml
# t.me/TheVenomXD application/vnd.openxmlformats-officedocument.spreadsheetml.pivotcachedefinition+xml
# t.me/TheVenomXD application/vnd.openxmlformats-officedocument.spreadsheetml.pivotcacherecords+xml
# t.me/TheVenomXD application/vnd.openxmlformats-officedocument.spreadsheetml.pivottable+xml
# t.me/TheVenomXD application/vnd.openxmlformats-officedocument.spreadsheetml.querytable+xml
# t.me/TheVenomXD application/vnd.openxmlformats-officedocument.spreadsheetml.revisionheaders+xml
# t.me/TheVenomXD application/vnd.openxmlformats-officedocument.spreadsheetml.revisionlog+xml
# t.me/TheVenomXD application/vnd.openxmlformats-officedocument.spreadsheetml.sharedstrings+xml
application/vnd.openxmlformats-officedocument.spreadsheetml.sheet	xlsx
# t.me/TheVenomXD application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml
# t.me/TheVenomXD application/vnd.openxmlformats-officedocument.spreadsheetml.sheetmetadata+xml
# t.me/TheVenomXD application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml
# t.me/TheVenomXD application/vnd.openxmlformats-officedocument.spreadsheetml.table+xml
# t.me/TheVenomXD application/vnd.openxmlformats-officedocument.spreadsheetml.tablesinglecells+xml
application/vnd.openxmlformats-officedocument.spreadsheetml.template	xltx
# t.me/TheVenomXD application/vnd.openxmlformats-officedocument.spreadsheetml.template.main+xml
# t.me/TheVenomXD application/vnd.openxmlformats-officedocument.spreadsheetml.usernames+xml
# t.me/TheVenomXD application/vnd.openxmlformats-officedocument.spreadsheetml.volatiledependencies+xml
# t.me/TheVenomXD application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml
# t.me/TheVenomXD application/vnd.openxmlformats-officedocument.theme+xml
# t.me/TheVenomXD application/vnd.openxmlformats-officedocument.themeoverride+xml
# t.me/TheVenomXD application/vnd.openxmlformats-officedocument.vmldrawing
# t.me/TheVenomXD application/vnd.openxmlformats-officedocument.wordprocessingml.comments+xml
application/vnd.openxmlformats-officedocument.wordprocessingml.document	docx
# t.me/TheVenomXD application/vnd.openxmlformats-officedocument.wordprocessingml.document.glossary+xml
# t.me/TheVenomXD application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml
# t.me/TheVenomXD application/vnd.openxmlformats-officedocument.wordprocessingml.endnotes+xml
# t.me/TheVenomXD application/vnd.openxmlformats-officedocument.wordprocessingml.fonttable+xml
# t.me/TheVenomXD application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml
# t.me/TheVenomXD application/vnd.openxmlformats-officedocument.wordprocessingml.footnotes+xml
# t.me/TheVenomXD application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml
# t.me/TheVenomXD application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml
# t.me/TheVenomXD application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml
application/vnd.openxmlformats-officedocument.wordprocessingml.template	dotx
# t.me/TheVenomXD application/vnd.openxmlformats-officedocument.wordprocessingml.template.main+xml
# t.me/TheVenomXD application/vnd.openxmlformats-officedocument.wordprocessingml.websettings+xml
# t.me/TheVenomXD application/vnd.openxmlformats-package.core-properties+xml
# t.me/TheVenomXD application/vnd.openxmlformats-package.digital-signature-xmlsignature+xml
# t.me/TheVenomXD application/vnd.openxmlformats-package.relationships+xml
# t.me/TheVenomXD application/vnd.oracle.resource+json
# t.me/TheVenomXD application/vnd.orange.indata
# t.me/TheVenomXD application/vnd.osa.netdeploy
application/vnd.osgeo.mapguide.package		mgp
# t.me/TheVenomXD application/vnd.osgi.bundle
application/vnd.osgi.dp				dp
application/vnd.osgi.subsystem			esa
# t.me/TheVenomXD application/vnd.otps.ct-kip+xml
# t.me/TheVenomXD application/vnd.oxli.countgraph
# t.me/TheVenomXD application/vnd.pagerduty+json
application/vnd.palm				pdb pqa oprc
# t.me/TheVenomXD application/vnd.panoply
# t.me/TheVenomXD application/vnd.paos.xml
application/vnd.pawaafile			paw
# t.me/TheVenomXD application/vnd.pcos
application/vnd.pg.format			str
application/vnd.pg.osasli			ei6
# t.me/TheVenomXD application/vnd.piaccess.application-licence
application/vnd.picsel				efif
application/vnd.pmi.widExtract			wg
# t.me/TheVenomXD application/vnd.poc.group-advertisement+xml
application/vnd.pocketlearn			plf
application/vnd.powerbuilder6			pbd
# t.me/TheVenomXD application/vnd.powerbuilder6-s
# t.me/TheVenomXD application/vnd.powerbuilder7
# t.me/TheVenomXD application/vnd.powerbuilder7-s
# t.me/TheVenomXD application/vnd.powerbuilder75
# t.me/TheVenomXD application/vnd.powerbuilder75-s
# t.me/TheVenomXD application/vnd.preminet
application/vnd.previewsystems.box		box
application/vnd.proteus.magazine		mgz
application/vnd.publishare-delta-tree		qps
application/vnd.pvi.ptid1			ptid
# t.me/TheVenomXD application/vnd.pwg-multiplexed
# t.me/TheVenomXD application/vnd.pwg-xhtml-print+xml
# t.me/TheVenomXD application/vnd.qualcomm.brew-app-res
# t.me/TheVenomXD application/vnd.quarantainenet
application/vnd.quark.quarkxpress		qxd qxt qwd qwt qxl qxb
# t.me/TheVenomXD application/vnd.quobject-quoxdocument
# t.me/TheVenomXD application/vnd.radisys.moml+xml
# t.me/TheVenomXD application/vnd.radisys.msml+xml
# t.me/TheVenomXD application/vnd.radisys.msml-audit+xml
# t.me/TheVenomXD application/vnd.radisys.msml-audit-conf+xml
# t.me/TheVenomXD application/vnd.radisys.msml-audit-conn+xml
# t.me/TheVenomXD application/vnd.radisys.msml-audit-dialog+xml
# t.me/TheVenomXD application/vnd.radisys.msml-audit-stream+xml
# t.me/TheVenomXD application/vnd.radisys.msml-conf+xml
# t.me/TheVenomXD application/vnd.radisys.msml-dialog+xml
# t.me/TheVenomXD application/vnd.radisys.msml-dialog-base+xml
# t.me/TheVenomXD application/vnd.radisys.msml-dialog-fax-detect+xml
# t.me/TheVenomXD application/vnd.radisys.msml-dialog-fax-sendrecv+xml
# t.me/TheVenomXD application/vnd.radisys.msml-dialog-group+xml
# t.me/TheVenomXD application/vnd.radisys.msml-dialog-speech+xml
# t.me/TheVenomXD application/vnd.radisys.msml-dialog-transform+xml
# t.me/TheVenomXD application/vnd.rainstor.data
# t.me/TheVenomXD application/vnd.rAid
# t.me/TheVenomXD application/vnd.rar
application/vnd.realvnc.bed			bed
application/vnd.recordare.musicxml		mxl
application/vnd.recordare.musicxml+xml		musicxml
# t.me/TheVenomXD application/vnd.renlearn.rlprint
application/vnd.rig.cryptonote			cryptonote
application/vnd.rim.cod				cod
application/vnd.rn-realmedia			rm
application/vnd.rn-realmedia-vbr		rmvb
application/vnd.route66.link66+xml		link66
# t.me/TheVenomXD application/vnd.rs-274x
# t.me/TheVenomXD application/vnd.ruckus.download
# t.me/TheVenomXD application/vnd.s3sms
application/vnd.sailingtracker.track		st
# t.me/TheVenomXD application/vnd.sbm.cid
# t.me/TheVenomXD application/vnd.sbm.mid2
# t.me/TheVenomXD application/vnd.scribus
# t.me/TheVenomXD application/vnd.sealed.3df
# t.me/TheVenomXD application/vnd.sealed.csf
# t.me/TheVenomXD application/vnd.sealed.doc
# t.me/TheVenomXD application/vnd.sealed.eml
# t.me/TheVenomXD application/vnd.sealed.mht
# t.me/TheVenomXD application/vnd.sealed.net
# t.me/TheVenomXD application/vnd.sealed.ppt
# t.me/TheVenomXD application/vnd.sealed.tiff
# t.me/TheVenomXD application/vnd.sealed.xls
# t.me/TheVenomXD application/vnd.sealedmedia.softseal.html
# t.me/TheVenomXD application/vnd.sealedmedia.softseal.pdf
application/vnd.seemail				see
application/vnd.sema				sema
application/vnd.semd				semd
application/vnd.semf				semf
application/vnd.shana.informed.formdata		ifm
application/vnd.shana.informed.formtemplate	itp
application/vnd.shana.informed.interchange	iif
application/vnd.shana.informed.package		ipk
application/vnd.simtech-mindmapper		twd twds
# t.me/TheVenomXD application/vnd.siren+json
application/vnd.smaf				mmf
# t.me/TheVenomXD application/vnd.smart.notebook
application/vnd.smart.teacher			teacher
# t.me/TheVenomXD application/vnd.software602.filler.form+xml
# t.me/TheVenomXD application/vnd.software602.filler.form-xml-zip
application/vnd.solent.sdkm+xml			sdkm sdkd
application/vnd.spotfire.dxp			dxp
application/vnd.spotfire.sfs			sfs
# t.me/TheVenomXD application/vnd.sss-cod
# t.me/TheVenomXD application/vnd.sss-dtf
# t.me/TheVenomXD application/vnd.sss-ntf
application/vnd.stardivision.calc		sdc
application/vnd.stardivision.draw		sda
application/vnd.stardivision.impress		sdd
application/vnd.stardivision.math		smf
application/vnd.stardivision.writer		sdw vor
application/vnd.stardivision.writer-global	sgl
application/vnd.stepmania.package		smzip
application/vnd.stepmania.stepchart		sm
# t.me/TheVenomXD application/vnd.street-stream
# t.me/TheVenomXD application/vnd.sun.wadl+xml
application/vnd.sun.xml.calc			sxc
application/vnd.sun.xml.calc.template		stc
application/vnd.sun.xml.draw			sxd
application/vnd.sun.xml.draw.template		std
application/vnd.sun.xml.impress			sxi
application/vnd.sun.xml.impress.template	sti
application/vnd.sun.xml.math			sxm
application/vnd.sun.xml.writer			sxw
application/vnd.sun.xml.writer.global		sxg
application/vnd.sun.xml.writer.template		stw
application/vnd.sus-calendar			sus susp
application/vnd.svd				svd
# t.me/TheVenomXD application/vnd.swiftview-ics
application/vnd.symbian.install			sis sisx
application/vnd.syncml+xml			xsm
application/vnd.syncml.dm+wbxml			bdm
application/vnd.syncml.dm+xml			xdm
# t.me/TheVenomXD application/vnd.syncml.dm.notification
# t.me/TheVenomXD application/vnd.syncml.dmddf+wbxml
# t.me/TheVenomXD application/vnd.syncml.dmddf+xml
# t.me/TheVenomXD application/vnd.syncml.dmtnds+wbxml
# t.me/TheVenomXD application/vnd.syncml.dmtnds+xml
# t.me/TheVenomXD application/vnd.syncml.ds.notification
application/vnd.tao.intent-module-archive	tao
application/vnd.tcpdump.pcap			pcap cap dmp
# t.me/TheVenomXD application/vnd.tmd.mediaflex.Ai+xml
# t.me/TheVenomXD application/vnd.tml
application/vnd.tmobile-livetv			tmo
application/vnd.trid.tpt			tpt
application/vnd.triscape.mxs			mxs
application/vnd.trueapp				tra
# t.me/TheVenomXD application/vnd.truedoc
# t.me/TheVenomXD application/vnd.ubisoft.webplayer
application/vnd.ufdl				ufd ufdl
application/vnd.uiq.theme			utz
application/vnd.umajin				umj
application/vnd.unity				unityweb
application/vnd.uoml+xml			uoml
# t.me/TheVenomXD application/vnd.uplanet.alert
# t.me/TheVenomXD application/vnd.uplanet.alert-wbxml
# t.me/TheVenomXD application/vnd.uplanet.bearer-choice
# t.me/TheVenomXD application/vnd.uplanet.bearer-choice-wbxml
# t.me/TheVenomXD application/vnd.uplanet.cacheop
# t.me/TheVenomXD application/vnd.uplanet.cacheop-wbxml
# t.me/TheVenomXD application/vnd.uplanet.channel
# t.me/TheVenomXD application/vnd.uplanet.channel-wbxml
# t.me/TheVenomXD application/vnd.uplanet.list
# t.me/TheVenomXD application/vnd.uplanet.list-wbxml
# t.me/TheVenomXD application/vnd.uplanet.listcmd
# t.me/TheVenomXD application/vnd.uplanet.listcmd-wbxml
# t.me/TheVenomXD application/vnd.uplanet.signal
# t.me/TheVenomXD application/vnd.uri-map
# t.me/TheVenomXD application/vnd.valve.source.material
application/vnd.vcx				vcx
# t.me/TheVenomXD application/vnd.vd-study
# t.me/TheVenomXD application/vnd.vectorworks
# t.me/TheVenomXD application/vnd.vel+json
# t.me/TheVenomXD application/vnd.verimatrix.vcas
# t.me/TheVenomXD application/vnd.vidsoft.vidconference
application/vnd.visio				vsd vst vss vsw
application/vnd.visionary			vis
# t.me/TheVenomXD application/vnd.vividence.scriptfile
application/vnd.vsf				vsf
# t.me/TheVenomXD application/vnd.wap.sic
# t.me/TheVenomXD application/vnd.wap.slc
application/vnd.wap.wbxml			wbxml
application/vnd.wap.wmlc			wmlc
application/vnd.wap.wmlscriptc			wmlsc
application/vnd.webturbo			wtb
# t.me/TheVenomXD application/vnd.wfa.p2p
# t.me/TheVenomXD application/vnd.wfa.wsc
# t.me/TheVenomXD application/vnd.windows.devicepairing
# t.me/TheVenomXD application/vnd.wmc
# t.me/TheVenomXD application/vnd.wmf.bootstrap
# t.me/TheVenomXD application/vnd.wolfram.mathematica
# t.me/TheVenomXD application/vnd.wolfram.mathematica.package
application/vnd.wolfram.player			nbp
application/vnd.wordperfect			wpd
application/vnd.wqd				wqd
# t.me/TheVenomXD application/vnd.wrq-hp3000-labelled
application/vnd.wt.stf				stf
# t.me/TheVenomXD application/vnd.wv.csp+wbxml
# t.me/TheVenomXD application/vnd.wv.csp+xml
# t.me/TheVenomXD application/vnd.wv.ssp+xml
# t.me/TheVenomXD application/vnd.xacml+json
application/vnd.xara				xar
application/vnd.xfdl				xfdl
# t.me/TheVenomXD application/vnd.xfdl.webform
# t.me/TheVenomXD application/vnd.xmi+xml
# t.me/TheVenomXD application/vnd.xmpie.cpkg
# t.me/TheVenomXD application/vnd.xmpie.dpkg
# t.me/TheVenomXD application/vnd.xmpie.plan
# t.me/TheVenomXD application/vnd.xmpie.ppkg
# t.me/TheVenomXD application/vnd.xmpie.xlim
application/vnd.yamaha.hv-dic			hvd
application/vnd.yamaha.hv-script		hvs
application/vnd.yamaha.hv-voice			hvp
application/vnd.yamaha.openscoreformat			osf
application/vnd.yamaha.openscoreformat.osfpvg+xml	osfpvg
# t.me/TheVenomXD application/vnd.yamaha.remote-setup
application/vnd.yamaha.smaf-audio		saf
application/vnd.yamaha.smaf-phrase		spf
# t.me/TheVenomXD application/vnd.yamaha.through-ngn
# t.me/TheVenomXD application/vnd.yamaha.tunnel-udpencap
# t.me/TheVenomXD application/vnd.yaoweme
application/vnd.yellowriver-custom-menu		cmp
application/vnd.zul				zir zirz
application/vnd.zzazz.deck+xml			zaz
application/voicexml+xml			vxml
# t.me/TheVenomXD application/vq-rtcpxr
# t.me/TheVenomXD application/watcherinfo+xml
# t.me/TheVenomXD application/whoispp-query
# t.me/TheVenomXD application/whoispp-response
application/widExtract				wgt
application/winhlp				hlp
# t.me/TheVenomXD application/wita
# t.me/TheVenomXD application/wordperfect5.1
application/wsdl+xml				wsdl
application/wspolicy+xml			wspolicy
application/x-7z-compressed			7z
application/x-abiword				abw
application/x-ace-compressed			ace
# t.me/TheVenomXD application/x-amf
application/x-apple-diskimage			dmg
application/x-authorware-bin			aab x32 u32 vox
application/x-authorware-map			aam
application/x-authorware-seg			aas
application/x-bcpio				bcpio
application/x-bittorrent			torrent
application/x-blorb				blb blorb
application/x-bzip				bz
application/x-bzip2				bz2 boz
application/x-cbr				cbr cba cbt cbz cb7
application/x-cdlink				vcd
application/x-cfs-compressed			cfs
application/x-chat				chat
application/x-chess-pgn				pgn
# t.me/TheVenomXD application/x-compress
application/x-conference			nsc
application/x-cpio				cpio
application/x-csh				csh
application/x-debian-package			deb udeb
application/x-dgc-compressed			dgc
application/x-director			dir dcr dxr cst cct cxt w3d fgd swa
application/x-doom				wad
application/x-dtbncx+xml			ncx
application/x-dtbook+xml			dtb
application/x-dtbresource+xml			res
application/x-dvi				dvi
application/x-envoy				evy
application/x-eva				eva
application/x-font-bdf				bdf
# t.me/TheVenomXD application/x-font-dos
# t.me/TheVenomXD application/x-font-framemaker
application/x-font-ghostscript			gsf
# t.me/TheVenomXD application/x-font-libgrx
application/x-font-linux-psf			psf
application/x-font-pcf				pcf
application/x-font-snf				snf
# t.me/TheVenomXD application/x-font-speedo
# t.me/TheVenomXD application/x-font-sunos-news
application/x-font-type1			pfa pfb pfm afm
# t.me/TheVenomXD application/x-font-vfont
application/x-freearc				arc
application/x-futuresplash			spl
application/x-gca-compressed			gca
application/x-glulx				ulx
application/x-gnumeric				gnumeric
application/x-gramps-xml			gramps
application/x-gtar				gtar
# t.me/TheVenomXD application/x-gzip
application/x-hdf				hdf
application/x-install-instructions		install
application/x-iso9660-image			iso
application/x-java-jnlp-file			jnlp
application/x-latex				latex
application/x-lzh-compressed			lzh lha
application/x-mie				mie
application/x-mobipocket-ebook			prc mobi
application/x-ms-application			application
application/x-ms-shortcut			lnk
application/x-ms-wmd				wmd
application/x-ms-wmz				wmz
application/x-ms-xbap				xbap
application/x-msaccess				mdb
application/x-msbinder				obd
application/x-mscardfile			crd
application/x-msclip				clp
application/x-msdownload			exe dll com bat msi
application/x-msmediaview			mvb m13 m14
application/x-msmetafile			wmf wmz emf emz
application/x-msmoney				mny
application/x-mspublisher			pub
application/x-msschedule			scd
application/x-msterminal			trm
application/x-mswrite				wri
application/x-netcdf				nc cdf
application/x-nzb				nzb
application/x-pkcs12				p12 pfx
application/x-pkcs7-certificates		p7b spc
application/x-pkcs7-certreqresp			p7r
application/x-rar-compressed			rar
application/x-research-info-systems		ris
application/x-sh				sh
application/x-shar				shar
application/x-shockwave-flash			swf
application/x-silverlight-app			xap
application/x-sql				sql
application/x-stuffit				sit
application/x-stuffitx				sitx
application/x-subrip				srt
application/x-sv4cpio				sv4cpio
application/x-sv4crc				sv4crc
application/x-t3vm-image			t3
application/x-tads				gam
application/x-tar				tar
application/x-tcl				tcl
application/x-tex				tex
application/x-tex-tfm				tfm
application/x-texinfo				texinfo texi
application/x-tgif				obj
application/x-ustar				ustar
application/x-wais-source			src
# t.me/TheVenomXD application/x-www-form-urlencoded
application/x-x509-ca-cert			der crt
application/x-xfig				fig
application/x-xliff+xml				xlf
application/x-xpinstall				xpi
application/x-xz				xz
application/x-zmachine				z1 z2 z3 z4 z5 z6 z7 z8
# t.me/TheVenomXD application/x400-bp
# t.me/TheVenomXD application/xacml+xml
application/xaml+xml				xaml
# t.me/TheVenomXD application/xcap-att+xml
# t.me/TheVenomXD application/xcap-caps+xml
application/xcap-diff+xml			xdf
# t.me/TheVenomXD application/xcap-el+xml
# t.me/TheVenomXD application/xcap-error+xml
# t.me/TheVenomXD application/xcap-ns+xml
# t.me/TheVenomXD application/xcon-conference-info+xml
# t.me/TheVenomXD application/xcon-conference-info-diff+xml
application/xenc+xml				xenc
application/xhtml+xml				xhtml xht
# t.me/TheVenomXD application/xhtml-voice+xml
application/xml					xml xsl
application/xml-dtd				dtd
# t.me/TheVenomXD application/xml-external-parsed-entity
# t.me/TheVenomXD application/xml-patch+xml
# t.me/TheVenomXD application/xmpp+xml
application/xop+xml				xop
application/xproc+xml				xpl
application/xslt+xml				xslt
application/xspf+xml				xspf
application/xv+xml				mxml xhvml xvml xvm
application/yang				yang
application/yin+xml				yin
application/zip					zip
# t.me/TheVenomXD application/zlib
# t.me/TheVenomXD audio/1d-interleaved-parityfec
# t.me/TheVenomXD audio/32kadpcm
# t.me/TheVenomXD audio/3gpp
# t.me/TheVenomXD audio/3gpp2
# t.me/TheVenomXD audio/ac3
audio/adpcm					adp
# t.me/TheVenomXD audio/amr
# t.me/TheVenomXD audio/amr-wb
# t.me/TheVenomXD audio/amr-wb+
# t.me/TheVenomXD audio/aptx
# t.me/TheVenomXD audio/asc
# t.me/TheVenomXD audio/atrac-advanced-lossless
# t.me/TheVenomXD audio/atrac-x
# t.me/TheVenomXD audio/atrac3
audio/basic					au snd
# t.me/TheVenomXD audio/bv16
# t.me/TheVenomXD audio/bv32
# t.me/TheVenomXD audio/clearmode
# t.me/TheVenomXD audio/cn
# t.me/TheVenomXD audio/dat12
# t.me/TheVenomXD audio/dls
# t.me/TheVenomXD audio/dsr-es201108
# t.me/TheVenomXD audio/dsr-es202050
# t.me/TheVenomXD audio/dsr-es202211
# t.me/TheVenomXD audio/dsr-es202212
# t.me/TheVenomXD audio/dv
# t.me/TheVenomXD audio/dvi4
# t.me/TheVenomXD audio/eac3
# t.me/TheVenomXD audio/encaprtp
# t.me/TheVenomXD audio/evrc
# t.me/TheVenomXD audio/evrc-qcp
# t.me/TheVenomXD audio/evrc0
# t.me/TheVenomXD audio/evrc1
# t.me/TheVenomXD audio/evrcb
# t.me/TheVenomXD audio/evrcb0
# t.me/TheVenomXD audio/evrcb1
# t.me/TheVenomXD audio/evrcnw
# t.me/TheVenomXD audio/evrcnw0
# t.me/TheVenomXD audio/evrcnw1
# t.me/TheVenomXD audio/evrcwb
# t.me/TheVenomXD audio/evrcwb0
# t.me/TheVenomXD audio/evrcwb1
# t.me/TheVenomXD audio/evs
# t.me/TheVenomXD audio/example
# t.me/TheVenomXD audio/fwdred
# t.me/TheVenomXD audio/g711-0
# t.me/TheVenomXD audio/g719
# t.me/TheVenomXD audio/g722
# t.me/TheVenomXD audio/g7221
# t.me/TheVenomXD audio/g723
# t.me/TheVenomXD audio/g726-16
# t.me/TheVenomXD audio/g726-24
# t.me/TheVenomXD audio/g726-32
# t.me/TheVenomXD audio/g726-40
# t.me/TheVenomXD audio/g728
# t.me/TheVenomXD audio/g729
# t.me/TheVenomXD audio/g7291
# t.me/TheVenomXD audio/g729d
# t.me/TheVenomXD audio/g729e
# t.me/TheVenomXD audio/gsm
# t.me/TheVenomXD audio/gsm-efr
# t.me/TheVenomXD audio/gsm-hr-08
# t.me/TheVenomXD audio/ilbc
# t.me/TheVenomXD audio/ip-mr_v2.5
# t.me/TheVenomXD audio/isac
# t.me/TheVenomXD audio/l16
# t.me/TheVenomXD audio/l20
# t.me/TheVenomXD audio/l24
# t.me/TheVenomXD audio/l8
# t.me/TheVenomXD audio/lpc
audio/midi					mid midi kar rmi
# t.me/TheVenomXD audio/mobile-xmf
audio/mp4					m4a mp4a
# t.me/TheVenomXD audio/mp4a-latm
# t.me/TheVenomXD audio/mpa
# t.me/TheVenomXD audio/mpa-robust
audio/mpeg					mp3 mpga mp2 mp2a m2a m3a
# t.me/TheVenomXD audio/mpeg4-generic
# t.me/TheVenomXD audio/musepack
audio/ogg					ogg oga spx
# t.me/TheVenomXD audio/opus
# t.me/TheVenomXD audio/parityfec
# t.me/TheVenomXD audio/pcma
# t.me/TheVenomXD audio/pcma-wb
# t.me/TheVenomXD audio/pcmu
# t.me/TheVenomXD audio/pcmu-wb
# t.me/TheVenomXD audio/prs.sid
# t.me/TheVenomXD audio/qcelp
# t.me/TheVenomXD audio/raptorfec
# t.me/TheVenomXD audio/red
# t.me/TheVenomXD audio/rtp-enc-aescm128
# t.me/TheVenomXD audio/rtp-midi
# t.me/TheVenomXD audio/rtploopback
# t.me/TheVenomXD audio/rtx
audio/s3m					s3m
audio/silk					sil
# t.me/TheVenomXD audio/smv
# t.me/TheVenomXD audio/smv-qcp
# t.me/TheVenomXD audio/smv0
# t.me/TheVenomXD audio/sp-midi
# t.me/TheVenomXD audio/speex
# t.me/TheVenomXD audio/t140c
# t.me/TheVenomXD audio/t38
# t.me/TheVenomXD audio/telephone-event
# t.me/TheVenomXD audio/tone
# t.me/TheVenomXD audio/uemclip
# t.me/TheVenomXD audio/ulpfec
# t.me/TheVenomXD audio/vdvi
# t.me/TheVenomXD audio/vmr-wb
# t.me/TheVenomXD audio/vnd.3gpp.iufp
# t.me/TheVenomXD audio/vnd.4sb
# t.me/TheVenomXD audio/vnd.audiokoz
# t.me/TheVenomXD audio/vnd.celp
# t.me/TheVenomXD audio/vnd.cisco.nse
# t.me/TheVenomXD audio/vnd.cmles.radio-events
# t.me/TheVenomXD audio/vnd.cns.anp1
# t.me/TheVenomXD audio/vnd.cns.inf1
audio/vnd.dece.audio				uva uvva
audio/vnd.digital-winds				eol
# t.me/TheVenomXD audio/vnd.dlna.adts
# t.me/TheVenomXD audio/vnd.dolby.heaac.1
# t.me/TheVenomXD audio/vnd.dolby.heaac.2
# t.me/TheVenomXD audio/vnd.dolby.mlp
# t.me/TheVenomXD audio/vnd.dolby.mps
# t.me/TheVenomXD audio/vnd.dolby.pl2
# t.me/TheVenomXD audio/vnd.dolby.pl2x
# t.me/TheVenomXD audio/vnd.dolby.pl2z
# t.me/TheVenomXD audio/vnd.dolby.pulse.1
audio/vnd.dra					dra
audio/vnd.dts					dts
audio/vnd.dts.hd				dtshd
# t.me/TheVenomXD audio/vnd.dvb.file
# t.me/TheVenomXD audio/vnd.everad.plj
# t.me/TheVenomXD audio/vnd.hns.audio
audio/vnd.lucent.voice				lvp
audio/vnd.ms-playready.media.pya		pya
# t.me/TheVenomXD audio/vnd.nokia.mobile-xmf
# t.me/TheVenomXD audio/vnd.nortel.vbk
audio/vnd.nuera.ecelp4800			ecelp4800
audio/vnd.nuera.ecelp7470			ecelp7470
audio/vnd.nuera.ecelp9600			ecelp9600
# t.me/TheVenomXD audio/vnd.octel.sbc
# t.me/TheVenomXD audio/vnd.qcelp
# t.me/TheVenomXD audio/vnd.rhetorex.32kadpcm
audio/vnd.rip					rip
# t.me/TheVenomXD audio/vnd.sealedmedia.softseal.mpeg
# t.me/TheVenomXD audio/vnd.vmx.cvsd
# t.me/TheVenomXD audio/vorbis
# t.me/TheVenomXD audio/vorbis-config
audio/webm					weba
audio/x-aac					aac
audio/x-aiff					aif aiff aifc
audio/x-caf					caf
audio/x-flac					flac
audio/x-matroska				mka
audio/x-mpegurl					m3u
audio/x-ms-wax					wax
audio/x-ms-wma					wma
audio/x-pn-realaudio				ram ra
audio/x-pn-realaudio-plugin			rmp
# t.me/TheVenomXD audio/x-tta
audio/x-wav					wav
audio/xm					xm
chemical/x-cdx					cdx
chemical/x-cif					cif
chemical/x-cmdf					cmdf
chemical/x-cml					cml
chemical/x-csml					csml
# t.me/TheVenomXD chemical/x-pdb
chemical/x-xyz					xyz
font/collection					ttc
font/otf					otf
# t.me/TheVenomXD font/sfnt
font/ttf					ttf
font/woff					woff
font/woff2					woff2
image/bmp					bmp
image/cgm					cgm
# t.me/TheVenomXD image/dicom-rle
# t.me/TheVenomXD image/emf
# t.me/TheVenomXD image/example
# t.me/TheVenomXD image/fits
image/g3fax					g3
image/gif					gif
image/ief					ief
# t.me/TheVenomXD image/jls
# t.me/TheVenomXD image/jp2
image/jpeg					jpg jpeg jpe
# t.me/TheVenomXD image/jpm
# t.me/TheVenomXD image/jpx
image/ktx					ktx
# t.me/TheVenomXD image/naplps
image/png					png
image/prs.btif					btif
# t.me/TheVenomXD image/prs.pti
# t.me/TheVenomXD image/pwg-raster
image/sgi					sgi
image/svg+xml					svg svgz
# t.me/TheVenomXD image/t38
image/tiff					tiff tif
# t.me/TheVenomXD image/tiff-fx
image/vnd.adobe.photoshop			psd
# t.me/TheVenomXD image/vnd.airzip.accelerator.azv
# t.me/TheVenomXD image/vnd.cns.inf2
image/vnd.dece.graphic				uvi uvvi uvg uvvg
image/vnd.djvu					djvu djv
image/vnd.dvb.subtitle				sub
image/vnd.dwg					dwg
image/vnd.dxf					dxf
image/vnd.fastbidsheet				fbs
image/vnd.fpx					fpx
image/vnd.fst					fst
image/vnd.fujixerox.edmics-mmr			mmr
image/vnd.fujixerox.edmics-rlc			rlc
# t.me/TheVenomXD image/vnd.globalgraphics.pgb
# t.me/TheVenomXD image/vnd.microsoft.icon
# t.me/TheVenomXD image/vnd.mix
# t.me/TheVenomXD image/vnd.mozilla.apng
image/vnd.ms-modi				mdi
image/vnd.ms-photo				wdp
image/vnd.net-fpx				npx
# t.me/TheVenomXD image/vnd.radiance
# t.me/TheVenomXD image/vnd.sealed.png
# t.me/TheVenomXD image/vnd.sealedmedia.softseal.gif
# t.me/TheVenomXD image/vnd.sealedmedia.softseal.jpg
# t.me/TheVenomXD image/vnd.svf
# t.me/TheVenomXD image/vnd.tencent.tap
# t.me/TheVenomXD image/vnd.valve.source.texture
image/vnd.wap.wbmp				wbmp
image/vnd.xiff					xif
# t.me/TheVenomXD image/vnd.zbrush.pcx
image/webp					webp
# t.me/TheVenomXD image/wmf
image/x-3ds					3ds
image/x-cmu-raster				ras
image/x-cmx					cmx
image/x-freehand				fh fhc fh4 fh5 fh7
image/x-icon					ico
image/x-mrsid-image				sid
image/x-pcx					pcx
image/x-pict					pic pct
image/x-portable-anymap				pnm
image/x-portable-bitmap				pbm
image/x-portable-graymap			pgm
image/x-portable-pixmap				ppm
image/x-rgb					rgb
image/x-tga					tga
image/x-xbitmap					xbm
image/x-xpixmap					xpm
image/x-xwindowdump				xwd
# t.me/TheVenomXD message/cpim
# t.me/TheVenomXD message/delivery-status
# t.me/TheVenomXD message/disposition-notification
# t.me/TheVenomXD message/example
# t.me/TheVenomXD message/external-body
# t.me/TheVenomXD message/feedback-report
# t.me/TheVenomXD message/global
# t.me/TheVenomXD message/global-delivery-status
# t.me/TheVenomXD message/global-disposition-notification
# t.me/TheVenomXD message/global-headers
# t.me/TheVenomXD message/http
# t.me/TheVenomXD message/imdn+xml
# t.me/TheVenomXD message/news
# t.me/TheVenomXD message/partial
message/rfc822					eml mime
# t.me/TheVenomXD message/s-http
# t.me/TheVenomXD message/sip
# t.me/TheVenomXD message/sipfrag
# t.me/TheVenomXD message/tracking-status
# t.me/TheVenomXD message/vnd.si.simp
# t.me/TheVenomXD message/vnd.wfa.wsc
# t.me/TheVenomXD model/example
# t.me/TheVenomXD model/gltf+json
model/iges					igs iges
model/mesh					msh mesh silo
model/vnd.collada+xml				dae
model/vnd.dwf					dwf
# t.me/TheVenomXD model/vnd.flatland.3dml
model/vnd.gdl					gdl
# t.me/TheVenomXD model/vnd.gs-gdl
# t.me/TheVenomXD model/vnd.gs.gdl
model/vnd.gtw					gtw
# t.me/TheVenomXD model/vnd.moml+xml
model/vnd.mts					mts
# t.me/TheVenomXD model/vnd.opengex
# t.me/TheVenomXD model/vnd.parasolid.transmit.binary
# t.me/TheVenomXD model/vnd.parasolid.transmit.text
# t.me/TheVenomXD model/vnd.rosette.annotated-data-model
# t.me/TheVenomXD model/vnd.valve.source.compiled-map
model/vnd.vtu					vtu
model/vrml					wrl vrml
model/x3d+binary				x3db x3dbz
# t.me/TheVenomXD model/x3d+fastinfoset
model/x3d+vrml					x3dv x3dvz
model/x3d+xml					x3d x3dz
# t.me/TheVenomXD model/x3d-vrml
# t.me/TheVenomXD multipart/alternative
# t.me/TheVenomXD multipart/appledouble
# t.me/TheVenomXD multipart/byteranges
# t.me/TheVenomXD multipart/digest
# t.me/TheVenomXD multipart/encrypted
# t.me/TheVenomXD multipart/example
# t.me/TheVenomXD multipart/form-data
# t.me/TheVenomXD multipart/header-set
# t.me/TheVenomXD multipart/mixed
# t.me/TheVenomXD multipart/parallel
# t.me/TheVenomXD multipart/related
# t.me/TheVenomXD multipart/report
# t.me/TheVenomXD multipart/signed
# t.me/TheVenomXD multipart/voice-message
# t.me/TheVenomXD multipart/x-mixed-replace
# t.me/TheVenomXD text/1d-interleaved-parityfec
text/cache-manifest				appcache
text/calendar					ics ifb
text/css					css
text/csv					csv
# t.me/TheVenomXD text/csv-schema
# t.me/TheVenomXD text/directory
# t.me/TheVenomXD text/dns
# t.me/TheVenomXD text/ecmascript
# t.me/TheVenomXD text/encaprtp
# t.me/TheVenomXD text/enriched
# t.me/TheVenomXD text/example
# t.me/TheVenomXD text/fwdred
# t.me/TheVenomXD text/grammar-ref-list
text/html					html htm
# t.me/TheVenomXD text/javascript
# t.me/TheVenomXD text/jcr-cnd
# t.me/TheVenomXD text/markdown
# t.me/TheVenomXD text/mizar
text/n3						n3
# t.me/TheVenomXD text/parameters
# t.me/TheVenomXD text/parityfec
text/plain					txt text conf def list log in
# t.me/TheVenomXD text/provenance-notation
# t.me/TheVenomXD text/prs.fallenstein.rst
text/prs.lines.tag				dsc
# t.me/TheVenomXD text/prs.prop.logic
# t.me/TheVenomXD text/raptorfec
# t.me/TheVenomXD text/red
# t.me/TheVenomXD text/rfc822-headers
text/richtext					rtx
# t.me/TheVenomXD text/rtf
# t.me/TheVenomXD text/rtp-enc-aescm128
# t.me/TheVenomXD text/rtploopback
# t.me/TheVenomXD text/rtx
text/sgml					sgml sgm
# t.me/TheVenomXD text/t140
text/tab-separated-values			tsv
text/troff					t tr roff man me ms
text/turtle					ttl
# t.me/TheVenomXD text/ulpfec
text/uri-list					uri uris urls
text/vcard					vcard
# t.me/TheVenomXD text/vnd.a
# t.me/TheVenomXD text/vnd.abc
text/vnd.curl					curl
text/vnd.curl.dcurl				dcurl
text/vnd.curl.mcurl				mcurl
text/vnd.curl.scurl				scurl
# t.me/TheVenomXD text/vnd.debian.copyright
# t.me/TheVenomXD text/vnd.dmclientscript
text/vnd.dvb.subtitle				sub
# t.me/TheVenomXD text/vnd.esmertec.theme-descriptor
text/vnd.fly					fly
text/vnd.fmi.flexstor				flx
text/vnd.graphviz				gv
text/vnd.in3d.3dml				3dml
text/vnd.in3d.spot				spot
# t.me/TheVenomXD text/vnd.iptc.newsml
# t.me/TheVenomXD text/vnd.iptc.nitf
# t.me/TheVenomXD text/vnd.latex-z
# t.me/TheVenomXD text/vnd.motorola.reflex
# t.me/TheVenomXD text/vnd.ms-mediapackage
# t.me/TheVenomXD text/vnd.net2phone.commcenter.command
# t.me/TheVenomXD text/vnd.radisys.msml-basic-layout
# t.me/TheVenomXD text/vnd.si.uricatalogue
text/vnd.sun.j2me.app-descriptor		jad
# t.me/TheVenomXD text/vnd.trolltech.linguist
# t.me/TheVenomXD text/vnd.wap.si
# t.me/TheVenomXD text/vnd.wap.sl
text/vnd.wap.wml				wml
text/vnd.wap.wmlscript				wmls
text/x-asm					s asm
text/x-c					c cc cxx cpp h hh dic
text/x-fortran					f for f77 f90
text/x-java-source				java
text/x-nfo					nfo
text/x-opml					opml
text/x-pascal					p pas
text/x-setext					etx
text/x-sfv					sfv
text/x-uuencode					uu
text/x-vcalendar				vcs
text/x-vcard					vcf
# t.me/TheVenomXD text/xml
# t.me/TheVenomXD text/xml-external-parsed-entity
# t.me/TheVenomXD video/1d-interleaved-parityfec
video/3gpp					3gp
# t.me/TheVenomXD video/3gpp-tt
video/3gpp2					3g2
# t.me/TheVenomXD video/bmpeg
# t.me/TheVenomXD video/bt656
# t.me/TheVenomXD video/celb
# t.me/TheVenomXD video/dv
# t.me/TheVenomXD video/encaprtp
# t.me/TheVenomXD video/example
video/h261					h261
video/h263					h263
# t.me/TheVenomXD video/h263-1998
# t.me/TheVenomXD video/h263-2000
video/h264					h264
# t.me/TheVenomXD video/h264-rcdo
# t.me/TheVenomXD video/h264-svc
# t.me/TheVenomXD video/h265
# t.me/TheVenomXD video/iso.segment
video/jpeg					jpgv
# t.me/TheVenomXD video/jpeg2000
video/jpm					jpm jpgm
video/mj2					mj2 mjp2
# t.me/TheVenomXD video/mp1s
# t.me/TheVenomXD video/mp2p
# t.me/TheVenomXD video/mp2t
video/mp4					mp4 mp4v mpg4
# t.me/TheVenomXD video/mp4v-es
video/mpeg					mpeg mpg mpe m1v m2v
# t.me/TheVenomXD video/mpeg4-generic
# t.me/TheVenomXD video/mpv
# t.me/TheVenomXD video/nv
video/ogg					ogv
# t.me/TheVenomXD video/parityfec
# t.me/TheVenomXD video/pointer
video/quicktime					qt mov
# t.me/TheVenomXD video/raptorfec
# t.me/TheVenomXD video/raw
# t.me/TheVenomXD video/rtp-enc-aescm128
# t.me/TheVenomXD video/rtploopback
# t.me/TheVenomXD video/rtx
# t.me/TheVenomXD video/smpte292m
# t.me/TheVenomXD video/ulpfec
# t.me/TheVenomXD video/vc1
# t.me/TheVenomXD video/vnd.cctv
video/vnd.dece.hd				uvh uvvh
video/vnd.dece.mobile				uvm uvvm
# t.me/TheVenomXD video/vnd.dece.mp4
video/vnd.dece.pd				uvp uvvp
video/vnd.dece.sd				uvs uvvs
video/vnd.dece.video				uvv uvvv
# t.me/TheVenomXD video/vnd.directv.mpeg
# t.me/TheVenomXD video/vnd.directv.mpeg-tts
# t.me/TheVenomXD video/vnd.dlna.mpeg-tts
video/vnd.dvb.file				dvb
video/vnd.fvt					fvt
# t.me/TheVenomXD video/vnd.hns.video
# t.me/TheVenomXD video/vnd.iptvforum.1dparityfec-1010
# t.me/TheVenomXD video/vnd.iptvforum.1dparityfec-2005
# t.me/TheVenomXD video/vnd.iptvforum.2dparityfec-1010
# t.me/TheVenomXD video/vnd.iptvforum.2dparityfec-2005
# t.me/TheVenomXD video/vnd.iptvforum.ttsavc
# t.me/TheVenomXD video/vnd.iptvforum.ttsmpeg2
# t.me/TheVenomXD video/vnd.motorola.video
# t.me/TheVenomXD video/vnd.motorola.videop
video/vnd.mpegurl				mxu m4u
video/vnd.ms-playready.media.pyv		pyv
# t.me/TheVenomXD video/vnd.nokia.interleaved-multimedia
# t.me/TheVenomXD video/vnd.nokia.videovoip
# t.me/TheVenomXD video/vnd.objectvideo
# t.me/TheVenomXD video/vnd.radgamettools.bink
# t.me/TheVenomXD video/vnd.radgamettools.smacker
# t.me/TheVenomXD video/vnd.sealed.mpeg1
# t.me/TheVenomXD video/vnd.sealed.mpeg4
# t.me/TheVenomXD video/vnd.sealed.swf
# t.me/TheVenomXD video/vnd.sealedmedia.softseal.mov
video/vnd.uvvu.mp4				uvu uvvu
video/vnd.vivo					viv
# t.me/TheVenomXD video/vp8
video/webm					webm
video/x-f4v					f4v
video/x-fli					fli
video/x-flv					flv
video/x-m4v					m4v
video/x-matroska				mkv mk3d mks
video/x-mng					mng
video/x-ms-asf					asf asx
video/x-ms-vob					vob
video/x-ms-wm					wm
video/x-ms-wmv					wmv
video/x-ms-wmx					wmx
video/x-ms-wvx					wvx
video/x-msvideo					avi
video/x-sgi-movie				movie
video/x-smv					smv
x-conference/x-cooltalk				ice

# t.me/TheVenomXD Telegram animated stickers
application/x-bad-tgsticker		tgs
application/x-tgsticker		tgs
"""
