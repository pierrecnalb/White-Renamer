#!/bin/bash
pylupdate5 whiterenamer/ui/i18n/tr.pro
lrelease whiterenamer/ui/i18n/tr_fr.ts -qm tr_fr.qm
pyrcc5 -o whiterenamer/ui/resource_rc.py whiterenamer/ui/resources.qrc
