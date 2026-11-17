#!/usr/bin/env python3
"""Builds dist/telemetry.svg (zine-style black & white stats card) from the GitHub GraphQL API."""
import json, os, random, datetime as dt, urllib.request

USER = os.environ.get("GH_USER", "NirajBera")
UPM = 2048
G = json.loads(r'''{"0":[1012,"M506 16Q283 16 162 -109Q40 -234 40 -469V-1263Q40 -1511 156 -1644Q271 -1776 506 -1776Q742 -1776 857 -1644Q972 -1511 972 -1263V-469Q972 -234 851 -109Q730 16 506 16ZM506 -308Q547 -308 570 -345Q593 -382 593 -428V-1297Q593 -1359 580 -1406Q566 -1452 506 -1452Q446 -1452 432 -1406Q419 -1359 419 -1297V-428Q419 -382 442 -345Q466 -308 506 -308Z"],"1":[677,"M243 0V-1356Q207 -1313 144 -1286Q81 -1260 25 -1260V-1541Q78 -1549 139 -1576Q200 -1602 252 -1648Q305 -1695 333 -1761H616V0Z"],"2":[1012,"M62 0V-84Q62 -215 102 -320Q143 -424 207 -514Q271 -603 342 -689Q411 -773 474 -862Q536 -950 576 -1054Q615 -1157 615 -1286Q615 -1348 596 -1392Q578 -1437 520 -1437Q432 -1437 432 -1280V-1065H62Q61 -1088 60 -1117Q58 -1146 58 -1173Q58 -1363 98 -1496Q138 -1628 240 -1698Q341 -1767 525 -1767Q744 -1767 866 -1644Q987 -1521 987 -1293Q987 -1138 947 -1022Q907 -905 841 -810Q775 -714 696 -619Q640 -552 588 -482Q535 -412 495 -332H975V0Z"],"3":[1012,"M484 20Q251 20 145 -103Q39 -226 39 -474V-658H400V-473Q400 -403 418 -354Q435 -306 496 -306Q558 -306 575 -358Q592 -411 592 -530V-574Q592 -665 562 -733Q531 -801 442 -801Q431 -801 422 -800Q414 -800 408 -799V-1115Q499 -1115 547 -1156Q595 -1196 595 -1291Q595 -1440 509 -1440Q453 -1440 434 -1396Q414 -1353 414 -1286V-1233H50Q49 -1245 48 -1262Q48 -1279 48 -1295Q48 -1537 161 -1650Q274 -1763 507 -1763Q957 -1763 957 -1295Q957 -1165 922 -1080Q887 -996 792 -962Q867 -926 903 -870Q939 -814 950 -731Q961 -648 961 -530Q961 -266 850 -123Q740 20 484 20Z"],"4":[1012,"M540 1V-278H18V-553L351 -1761H899V-572H993V-278H899V1ZM332 -572H540V-1459Z"],"5":[1012,"M506 25Q303 25 174 -76Q46 -176 46 -384V-646H412V-495Q412 -448 418 -404Q423 -360 443 -332Q463 -304 506 -304Q563 -304 581 -342Q599 -381 599 -441V-787Q599 -830 594 -872Q588 -914 569 -942Q550 -970 508 -970Q408 -970 408 -825H85V-1761H924V-1431H419V-1183Q445 -1215 490 -1240Q534 -1264 594 -1264Q714 -1264 790 -1218Q865 -1172 906 -1090Q946 -1008 962 -900Q977 -792 977 -668Q977 -509 960 -382Q944 -254 896 -163Q847 -72 754 -24Q660 25 506 25Z"],"6":[1012,"M529 16Q346 16 242 -46Q139 -109 96 -235Q54 -361 54 -549V-1025Q54 -1208 70 -1348Q85 -1488 134 -1583Q183 -1678 280 -1727Q377 -1776 539 -1776Q650 -1776 746 -1738Q842 -1699 901 -1622Q960 -1546 960 -1431V-1241H621V-1277Q621 -1321 616 -1365Q612 -1409 594 -1438Q576 -1467 533 -1467Q474 -1467 451 -1434Q428 -1402 428 -1341V-988Q453 -1035 503 -1064Q553 -1092 625 -1092Q771 -1092 850 -1034Q928 -975 958 -859Q988 -743 988 -569Q988 -393 945 -262Q902 -130 802 -57Q701 16 529 16ZM516 -308Q578 -308 590 -360Q602 -413 602 -495V-637Q602 -781 521 -781Q428 -781 428 -656V-438Q428 -308 516 -308Z"],"7":[1012,"M145 -1Q161 -247 214 -461Q267 -675 336 -860Q405 -1044 469 -1198L567 -1435H70V-1761H958V-1569Q958 -1463 923 -1355Q888 -1247 831 -1117Q707 -835 634 -556Q560 -276 543 -1Z"],"8":[1012,"M506 19Q258 19 152 -123Q46 -265 46 -525V-642Q46 -776 78 -859Q110 -942 196 -986Q115 -1019 81 -1096Q47 -1174 47 -1289V-1335Q47 -1569 164 -1676Q282 -1782 506 -1782Q736 -1782 850 -1672Q964 -1563 964 -1321Q964 -1194 934 -1108Q904 -1022 815 -984Q910 -935 938 -856Q966 -776 966 -642V-525Q966 -265 860 -123Q754 19 506 19ZM506 -1134Q599 -1134 599 -1302Q599 -1358 580 -1408Q560 -1458 506 -1458Q452 -1458 432 -1408Q413 -1358 413 -1302Q413 -1134 506 -1134ZM506 -329Q602 -329 602 -484V-645Q602 -725 580 -770Q559 -815 506 -815Q451 -815 431 -770Q411 -725 411 -645V-484Q411 -329 506 -329Z"],"9":[1012,"M503 16Q392 16 296 -22Q200 -61 141 -138Q82 -215 82 -329V-519H421V-483Q421 -439 426 -395Q430 -351 448 -322Q467 -293 509 -293Q568 -293 591 -326Q614 -358 614 -419V-772Q589 -726 539 -697Q489 -668 417 -668Q272 -668 193 -726Q114 -785 84 -901Q54 -1017 54 -1191Q54 -1367 97 -1498Q140 -1630 240 -1703Q341 -1776 513 -1776Q697 -1776 800 -1714Q903 -1651 946 -1526Q988 -1400 988 -1211V-735Q988 -552 972 -412Q957 -272 908 -177Q859 -82 762 -33Q665 16 503 16ZM521 -979Q614 -979 614 -1104V-1322Q614 -1452 526 -1452Q464 -1452 452 -1400Q440 -1347 440 -1265V-1123Q440 -979 521 -979Z"],"A":[994,"M30 0 200 -1760H797L964 0H631L606 -284H394L372 0ZM419 -565H579L502 -1460H486Z"],"B":[980,"M78 0V-1760H555Q747 -1760 834 -1666Q922 -1573 922 -1358V-1281Q922 -1157 878 -1080Q833 -1003 742 -979Q861 -949 902 -838Q942 -728 942 -569Q942 -398 910 -270Q878 -142 794 -71Q710 0 555 0ZM422 -1097H494Q543 -1097 557 -1135Q571 -1173 571 -1226V-1403Q571 -1488 496 -1488H422ZM457 -310Q594 -310 594 -440V-660Q594 -735 572 -778Q549 -822 487 -822H422V-312Q444 -310 457 -310Z"],"C":[971,"M488 16Q297 16 180 -103Q64 -222 64 -436V-1248Q64 -1504 166 -1640Q267 -1776 496 -1776Q621 -1776 718 -1730Q816 -1684 872 -1592Q928 -1501 928 -1362V-1058H578V-1318Q578 -1397 558 -1424Q538 -1452 496 -1452Q447 -1452 430 -1416Q413 -1381 413 -1322V-441Q413 -368 434 -338Q456 -308 496 -308Q541 -308 560 -345Q578 -382 578 -441V-758H932V-425Q932 -193 815 -88Q698 16 488 16Z"],"D":[1010,"M78 0V-1760H562Q752 -1760 848 -1654Q944 -1549 944 -1346V-522Q944 -272 856 -136Q769 0 550 0ZM432 -311H493Q590 -311 590 -405V-1313Q590 -1401 566 -1426Q543 -1452 471 -1452H432Z"],"E":[843,"M78 0V-1760H782V-1420H436V-1077H768V-746H436V-343H805V0Z"],"F":[817,"M78 0V-1760H782V-1417H432V-1137H764V-798H432V0Z"],"G":[993,"M441 16Q64 16 64 -524V-1283Q64 -1776 496 -1776Q674 -1776 769 -1704Q864 -1633 900 -1496Q936 -1359 936 -1162H592V-1318Q592 -1375 576 -1414Q561 -1452 512 -1452Q451 -1452 432 -1411Q412 -1370 412 -1321V-468Q412 -397 430 -352Q449 -308 503 -308Q559 -308 578 -352Q596 -397 596 -470V-721H502V-1025H932V0H791L731 -148Q639 16 441 16Z"],"H":[1022,"M78 0V-1760H428V-1131H594V-1760H944V0H594V-798H428V0Z"],"I":[464,"M62 0V-1760H402V0Z"],"J":[955,"M468 16Q349 16 251 -30Q153 -76 96 -166Q38 -257 38 -389V-830H386V-410Q386 -364 404 -336Q423 -308 464 -308Q543 -308 543 -405V-1760H898V-440Q898 -300 843 -198Q788 -95 691 -40Q594 16 468 16Z"],"K":[967,"M78 0V-1760H426V-1055L590 -1760H944L747 -954L985 0H620L428 -852V0Z"],"L":[814,"M78 0V-1760H430V-300H792V0Z"],"M":[1528,"M78 0V-1760H614L762 -687L909 -1760H1450V0H1128V-1268L926 0H610L396 -1268V0Z"],"N":[1020,"M78 0V-1760H440L602 -917V-1760H942V0H598L422 -880V0Z"],"O":[996,"M498 16Q287 16 176 -112Q64 -239 64 -480V-1316Q64 -1542 174 -1659Q285 -1776 498 -1776Q711 -1776 822 -1659Q932 -1542 932 -1316V-480Q932 -239 820 -112Q709 16 498 16ZM501 -308Q581 -308 581 -463V-1322Q581 -1452 503 -1452Q415 -1452 415 -1319V-461Q415 -379 435 -344Q455 -308 501 -308Z"],"P":[967,"M78 0V-1760H543Q689 -1760 774 -1695Q860 -1630 897 -1510Q934 -1390 934 -1224Q934 -1064 903 -946Q872 -827 792 -762Q713 -697 567 -697H424V0ZM424 -1013H444Q542 -1013 564 -1068Q586 -1123 586 -1230Q586 -1330 564 -1384Q543 -1439 463 -1439H424Z"],"Q":[1011,"M856 187 576 3Q528 16 477 16Q271 16 162 -106Q54 -228 54 -462V-1313Q54 -1540 166 -1658Q277 -1776 488 -1776Q699 -1776 810 -1658Q922 -1540 922 -1313V-462Q922 -244 824 -119L975 -23ZM488 -308Q526 -308 542 -336Q559 -364 564 -405Q568 -446 568 -484V-1307Q568 -1363 552 -1408Q537 -1452 486 -1452Q434 -1452 418 -1408Q402 -1365 402 -1308V-477Q402 -442 406 -402Q411 -363 429 -336Q447 -308 488 -308Z"],"R":[976,"M78 0V-1760H618Q753 -1760 822 -1698Q891 -1637 914 -1526Q938 -1416 938 -1267Q938 -1123 902 -1037Q865 -951 764 -918Q847 -901 880 -836Q914 -770 914 -666V0H567V-689Q567 -766 536 -784Q504 -803 434 -803V0ZM436 -1108H521Q594 -1108 594 -1267Q594 -1370 578 -1402Q562 -1434 518 -1434H436Z"],"S":[945,"M496 16Q255 16 148 -104Q42 -224 42 -486V-658H390V-438Q390 -377 408 -342Q427 -308 473 -308Q521 -308 540 -336Q558 -364 558 -428Q558 -509 542 -564Q526 -618 486 -668Q447 -717 377 -783L219 -933Q42 -1100 42 -1315Q42 -1540 146 -1658Q251 -1776 449 -1776Q691 -1776 792 -1647Q894 -1518 894 -1255H536V-1376Q536 -1412 516 -1432Q495 -1452 460 -1452Q418 -1452 398 -1428Q379 -1405 379 -1368Q379 -1331 399 -1288Q419 -1245 478 -1189L681 -994Q742 -936 793 -872Q844 -807 875 -722Q906 -636 906 -513Q906 -265 814 -124Q723 16 496 16Z"],"T":[810,"M229 0V-1422H20V-1760H790V-1422H581V0Z"],"U":[970,"M485 16Q265 16 161 -108Q57 -231 57 -471V-1760H399V-485Q399 -441 404 -400Q409 -360 427 -334Q445 -308 485 -308Q526 -308 544 -334Q562 -359 566 -400Q571 -441 571 -485V-1760H913V-471Q913 -231 809 -108Q705 16 485 16Z"],"V":[961,"M240 0 23 -1761H358L487 -563L602 -1761H937L720 0Z"],"W":[1458,"M216 0 27 -1760H371L468 -649L567 -1760H895L989 -649L1083 -1760H1431L1239 0H817L729 -847L645 0Z"],"X":[991,"M27 0 216 -933 66 -1761H410L501 -1156L582 -1761H927L777 -933L965 0H609L498 -688L384 0Z"],"Y":[914,"M291 0V-579L10 -1760H359L457 -1164L555 -1760H903L623 -579V0Z"],"Z":[840,"M32 0V-320L435 -1436H71V-1760H806V-1452L396 -324H789V0Z"]," ":[480,""],":":[495,"M68 -976V-1274H426V-976ZM68 -237V-535H426V-237Z"],"-":[637,"M60 -509V-741H576V-509Z"],"/":[830,"M29 0 439 -1767H803L392 0Z"],",":[484,"M116 235 182 -1H55V-299H429V-10L327 235Z"],".":[468,"M55 -1V-299H413V-1Z"],"+":[728,"M248 -301V-509H40V-741H248V-949H480V-741H688V-509H480V-301Z"]}''')  # Anton glyph outlines: char -> [advance, path]
Q = """query($login:String!){user(login:$login){followers{totalCount}
 repositories(ownerAffiliations:OWNER,privacy:PUBLIC,first:100){totalCount nodes{stargazerCount}}
 contributionsCollection{contributionCalendar{totalContributions weeks{contributionDays{date contributionCount}}}}}}"""


def fetch():
    fx = os.environ.get("FIXTURE")
    if fx:
        return json.load(open(fx))
    req = urllib.request.Request("https://api.github.com/graphql", data=json.dumps({"query": Q, "variables": {"login": USER}}).encode(),
                                 headers={"Authorization": "bearer " + os.environ["GH_TOKEN"], "Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req))


def public_calendar():
    """Contribution days as shown on the public profile page (includes private contributions when the
    profile has 'Private contributions' turned on). Returns [(date, count, row, col)] or [] on failure."""
    import re
    try:
        fx = os.environ.get("FIXTURE_HTML")
        if fx:
            html = open(fx, encoding="utf-8").read()
        else:
            req = urllib.request.Request(f"https://github.com/users/{USER}/contributions", headers={"User-Agent": "Mozilla/5.0 profile-readme"})
            html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")
        tips = {}
        for m in re.finditer(r'<tool-tip[^>]*for="(contribution-day-component-\d+-\d+)"[^>]*>\s*([^<]*?)\s*</tool-tip>', html):
            n = re.match(r"(\d+)", m.group(2))
            tips[m.group(1)] = int(n.group(1)) if n else 0
        out = []
        for m in re.finditer(r'<td[^>]*data-date="(\d{4}-\d\d-\d\d)"[^>]*id="(contribution-day-component-(\d+)-(\d+))"[^>]*data-level="(\d)"', html):
            cnt = tips.get(m.group(2), int(m.group(5)))
            out.append((m.group(1), cnt, int(m.group(3)), int(m.group(4))))
        return sorted(out) if len(out) > 300 else []
    except Exception as e:  # fall back to the API
        print("public calendar failed:", e)
        return []


def T(text, x, y, size, fill, anchor="start", ls=0):
    text = "".join(c if c in G else " " for c in str(text).upper())
    sc = size / UPM
    w = sum(G[c][0] for c in text) * sc + ls * (len(text) - 1)
    cx = x - (w if anchor == "end" else w / 2 if anchor == "middle" else 0)
    out = ""
    for c in text:
        if c != " ":
            out += f'<use href="#g{ord(c)}" transform="translate({cx:.1f} {y}) scale({sc:.4f})" fill="{fill}"/>'
        cx += G[c][0] * sc + ls
    return out


def torn(w, h, rnd, teeth=6):
    pts = [(0, 0)] + [(rnd.uniform(-5, 2), h * i / teeth) for i in range(1, teeth)] + [(0, h), (w, h)]
    pts += [(w + rnd.uniform(-2, 5), h * i / teeth) for i in range(teeth - 1, 0, -1)] + [(w, 0)]
    return " ".join(f"{a:.1f},{b:.1f}" for a, b in pts)


u = fetch()["data"]["user"]
cal = u["contributionsCollection"]["contributionCalendar"]
days = [d for w in cal["weeks"] for d in w["contributionDays"]]
today = dt.datetime.now(dt.timezone.utc).date().isoformat()
pub = public_calendar()
if pub:
    days = [{"date": d, "contributionCount": c} for d, c, _, _ in pub]
    cal = {"totalContributions": sum(c for _, c, _, _ in pub)}
days = [d for d in days if d["date"] <= today]
counts = [d["contributionCount"] for d in days]
longest = cur = 0
for c in counts:
    cur = cur + 1 if c else 0
    longest = max(longest, cur)
i = len(counts) - 1
if i >= 0 and counts[i] == 0:
    i -= 1
current = 0
while i >= 0 and counts[i]:
    current += 1
    i -= 1
stars = sum(n["stargazerCount"] for n in u["repositories"]["nodes"])
last30 = counts[-30:]
mx = max(last30 + [1])

W, H = 900, 350
BG, WH = "#0b0b0b", "#f5f5f0"
rnd = random.Random(4)
s = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><defs>'
     + "".join(f'<path id="g{ord(c)}" d="{v[1]}"/>' for c, v in G.items() if c != " ")
     + '<filter id="rough" x="-2%" y="-10%" width="104%" height="120%"><feTurbulence type="fractalNoise" baseFrequency=".05" numOctaves="2" seed="8"/><feDisplacementMap in="SourceGraphic" scale="3"/></filter>'
     '<filter id="grit" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="1.1" numOctaves="2" seed="2"/><feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 -1.2 .55"/></filter>'
     f'<clipPath id="cr"><rect width="{W}" height="{H}" rx="6"/></clipPath></defs><style>'
     '.wg{animation:wg 3.4s ease-in-out infinite;transform-box:fill-box;transform-origin:center}@keyframes wg{0%,100%{transform:rotate(-1.2deg)}50%{transform:rotate(1.2deg)}}'
     '.bar{transform-box:fill-box;transform-origin:bottom;animation:g 1.2s cubic-bezier(.2,.8,.2,1) both}@keyframes g{from{transform:scaleY(0)}to{transform:scaleY(1)}}</style>'
     f'<g clip-path="url(#cr)"><rect width="{W}" height="{H}" fill="{BG}"/>')
tiles = [("CONTRIBUTIONS", cal["totalContributions"], "LAST 12 MONTHS"), ("CURRENT STREAK", current, "DAYS IN A ROW"),
         ("LONGEST STREAK", longest, "DAYS, BEST RUN"), ("PUBLIC REPOS", u["repositories"]["totalCount"], f"{stars} STARS / {u['followers']['totalCount']} FOLLOWERS")]
for k, (lab, val, sub) in enumerate(tiles):
    inv = k % 2 == 1
    fill, ink, dim = (BG, WH, "#9a9a9a") if inv else (WH, BG, "#555555")
    x = 26 + k * 216
    st = f' stroke="{WH}" stroke-width="2"' if inv else ""
    s += (f'<g transform="translate({x} {22 + (8 if inv else 0)}) rotate({[-1.5, 1.2, -1, 1.6][k]} 100 66)"><g class="wg" style="animation-delay:{-k * .7:.1f}s">'
          f'<polygon points="{torn(200, 132, rnd, 7)}" fill="{fill}"{st}/>' + T(val, 16, 78, 66, ink) + T(lab, 16, 104, 14, ink, ls=1.5) + T(sub, 16, 122, 10.5, dim, ls=1) + '</g></g>')
s += T("LAST 30 DAYS", 26, 204, 18, WH, ls=2)
upd = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
s += T("UPDATED " + upd, 874, 202, 11, "#8a8a8a", "end", 1)
bw = (848 - 29 * 6) / 30
s += '<g filter="url(#rough)">'
for k, c in enumerate(last30):
    x = 26 + k * (bw + 6)
    if c:
        h = 10 + (c / mx) * 76
        s += f'<rect class="bar" x="{x:.1f}" y="{318 - h:.1f}" width="{bw:.1f}" height="{h:.1f}" fill="{WH}" style="animation-delay:{k * .03:.2f}s"/>'
    else:
        s += f'<rect x="{x:.1f}" y="314" width="{bw:.1f}" height="4" fill="#3a3a3a"/>'
s += '</g>'
for k, c in enumerate(last30):
    if c:
        h = 10 + (c / mx) * 76
        s += T(c, 26 + k * (bw + 6) + bw / 2, 310 - h, 11, WH, "middle")
s += T(days[-30]["date"] if len(days) >= 30 else "", 26, 338, 10, "#8a8a8a", ls=1) + T(days[-1]["date"], 874, 338, 10, "#8a8a8a", "end", 1)
s += f'<rect width="{W}" height="{H}" filter="url(#grit)" opacity=".13"/></g></svg>'
os.makedirs("dist", exist_ok=True)
open("dist/telemetry.svg", "w", encoding="utf-8").write(s)
print("telemetry ok", cal["totalContributions"], current, longest)
