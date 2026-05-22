from itertools import product
import mysql.connector
import scrapy
import json,os,re,gzip
from scrapy.cmdline import execute
import datetime
from datetime import timedelta
from flipkart.items import FlipkartItem

#----Pagesave------
PAGE_SAVE_DIR=r"D:\apps\flipkart\flipkart\pagesave\pdp"
#helpe
def clean_empty(d):
    if not isinstance(d, dict):
        return d
    # Recursively clean nested dicts, then filter out empty/None values
    cleaned = {k: clean_empty(v) for k, v in d.items()}
    return {k: v for k, v in cleaned.items() if v not in (None, "", [], {})}

class Flipkart_PDP(scrapy.Spider):
    name = "pdp"
    # def __init__(self,end,start=0,*args,**kwargs):
    #     super().__init__(*args,**kwargs)
    #     self.start=int(start)
    #     self.end=int(end)

    def start_requests(self):
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="actowiz",
            database="flipkart"
        )

        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM product_links WHERE status='pending'")
        rows = cursor.fetchall()
        custom_settings = {
            'COOKIES_ENABLED': False,
            'HTTPERROR_ALLOW_ALL': True,  # don't silently drop non-200 responses
        }
        # Keep as raw string, just like your requests script uses data=payload
        payload={
            "pageUri": "/puma-printed-men-crew-neck-white-t-shirt/p/itm849b11d1793e4?pid=TSHHAFF9FWUSGDH5&lid=LSTTSHHAFF9FWUSGDH5A2NPCR&marketplace=FLIPKART&hl_lid=&q=puma+tshirt+for+men&store=clo%2Fash%2Fank%2Fedy&ctx=eyJkZWxpdmVyZWRCeSI6IiIsImRpc3BsYXlQcmljZSI6IjY3OSJ9&fm=eyJ3dHAiOiJwcm9kdWN0Q2FyZExpc3QiLCJwcnB0Ijoic3AiLCJtaWQiOiJQUk9EVUNUIn0",
            "pageContext": {
                "pageHashKey": None,
                "slotContextMap": None,
                "paginationContextMap": None,
                "stateInfoMap": None,
                "slotIdInfoMap": None,
                "gamificationBUInfoMap": None,
                "paginatedFetch": False,
                "pageNumber": 1,
                "fetchAllPages": False,
                "networkSpeed": 17,
                "trackingContext": {
                    "context": {
                        "eVar51": "atlas_delivery_ATLAS_DELIVERY_pp",
                        "eVar61": "AS_QueryStore_OrganicAutoSuggest_0_12_na_na_ps"
                    }
                },
                "fetchSeoData": False,
                "ltcContext": None
            },
            "partnerContext": None,
            "locationContext": None,
            "requestContext": None
        }
        headers = {
            'Accept-Encoding': 'gzip',
            'at': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImQ2Yjk5NDViLWZmYTEtNGQ5ZC1iZDQyLTFkN2RmZTU4ZGNmYSJ9.eyJleHAiOjE3ODEwNjI1MjgsImlhdCI6MTc3OTMzNDUyOCwiaXNzIjoia2V2bGFyIiwianRpIjoiNGEwOTIzYWEtMzY0OS00NTdkLTk4OWItYWFiZjU0MTg2NjIxIiwidHlwZSI6IkFUIiwiZElkIjoiZDBmODhlNjU1ZTk3NzdlNzdkOThjNTcxOTVjNDkyNzYiLCJrZXZJZCI6IlZJOUM2MzdFODExQTE0NDcwMTlERTAxNzM3MkZFMzVBRDAiLCJ0SWQiOiJtYXBpIiwidnMiOiJMTyIsInoiOiJDSCIsIm0iOnRydWUsImdlbiI6MX0.XZ6KkOs15BNNe7OhcuhPpFqSljY7AKi7mAolhIK0ofs',
            'Connection': 'Keep-Alive',
            'Content-Type': 'application/json; charset=UTF-8',
            'Cookie': 'ud=4.rCYYxJcitGaaQYjQPydvdoC3ShcGlS4i15AUnHc6dSF-jDn0nj6MLA30fz1ZyVe2lyDiu5oQpwEjuv7wnQ52uBli_HJ3xwSSKuN-xyNrEkj2lzFy8C9_g-jPA-PG0pSIE9k_wO8yQc3Ow5Z2GXz4r2g6D1YuwfSWx5tkck99MKjj_0URDz13ndkKmPSB8DMNQJJBRdK3EdYJstgu4hMSAOTpjA4jV0Wj6YkjZyNGBl-9Zsll6HJBZCowXEobYkKCtl7lhqBGRenY20MbO10b_f5oq8magkO5AZRIjcR3e5cfZKCbIh69EIW-S4FLaME-YhCXX-jRHdaLslr-FMhoVLFbVYnf-jqOgakelPcw1VDUUTSrOmgFggVbcnGABPlebQh9te-jvF2bgTbsLb1xhKOBS_d2li--Wx2VZvqyYETdFyFIH45VhmkRThsmNiNUMPuficBoH1Qliq5CVuB0e8k_bvDF49ePMKFAN...; vd=VI9C637E811A1447019DE017372FE35AD0-1779334528108-2.1779344917.1779344917.151332620',
            'Host': '1.rome.api.flipkart.net',
            'Network-Type': 'wifi',
            'secureCookie': 'd1t15RD9jdkA/Pyg/FB1OPz8YMoHz+8jyHmcAGzQD8biZqXPDY4Oi4B5bgMIlyyZ2GOuoiu/vYQ9KU6Xr0oJjS1UKDQ==',
            'secureToken': 'AL0Xw2RxlzLDYc+CaN0TSMbIvFCHE44Ejodm1E272OcjD8EKeJ3t33Sk1ZylKLglOmfak0ic9+h2uTTBYthW5Q==',
            'sn': 'VI9C637E811A1447019DE017372FE35AD0.TOKBC4CDA804DCC4305B24D7B8DB07AF92E.1779344655966.LO',
            'User-Agent': 'okhttp/4.9.2',
            'X-AppSession-ID': 'bbbd5abe-023f-4428-b8b1-f2719c133d9a_1779344621780',
            'X-AR-AVAILABILITY': 'PRESENT',
            'x-atlas-versions': '30010000/3130100',
            'X-DLS': 'true',
            'X-Layout-Version': '{"appVersion":"910000","frameworkVersion":"1.0"}',
            'X-Location-Info': '{"cl":true}',
            'X-MULTIWIDGET-VERSION': '8.8.8',
            'X-NewRelic-ID': 'VwEHUVRUARABUVlaAAQGXlED',
            'x-request-metaInfo': '{"pageUri":"%2Freebok-printed-men-crew-neck-navy-blue-t-shirt%2Fp%2Fitm34525c8796e25%3Fpid%3DTSHHC7EXXBM9AH8Q%26marketplace%3DFLIPKART%26lid%3DLSTTSHHC7EXXBM9AH8QEGNCPH%26q%3Dreebok%2Bmens%2Btshirt%26fm%3DeyJ3dHAiOiJwcm9kdWN0Q2FyZExpc3QiLCJwcnB0Ijoic3AiLCJtaWQiOiJQUk9EVUNUIn0"}',
            'x-unified-atlas-version': '3130100.-1.-1.8008008.3000010.1003003',
            'X-User-Agent': 'Mozilla/5.0 (Linux; Android 9; ASUS_I003DD Build/PI) FKUA/Retail/3130100/Android/Mobile (Asus/ASUS_I003DD/d0f88e655e9777e77d98c57195c49276)',
            'X-Visit-Id': 'd0f88e655e9777e77d98c57195c49276-1779344621878'
        }

        print(f"Total Urls Fetched:{len(rows)}")
        for row in rows:
            product_url=row.get("url")
            print(product_url)
            pid=row.get("product_id")

            payload["pageUri"]=product_url
            yield scrapy.Request(url="https://1.rome.api.flipkart.net/4/page/fetch",
                method="POST",
                headers=headers,
                body=json.dumps(payload),           # ✅ raw string, same as requests' data=payload
                callback=self.parse,
                errback=self.errback_http,
                dont_filter=True,
                meta={"url":product_url,"product_id":pid}
            )


    def parse(self, response):
        product_url=response.meta.get("url")
        prod_id=response.meta.get("product_id")

        # ── FROM ITEMS.PY ────────────────────────────────────────────────────────
        item = FlipkartItem()
        # ── JSON load ────────────────────────────────────────────────────────
        try:
            data = json.loads(response.text)
            # ── Page save ────────────────────────────────────────────────────────
            try:

                os.makedirs(PAGE_SAVE_DIR, exist_ok=True)
                save_path = os.path.join(PAGE_SAVE_DIR, f"{prod_id}.json.gz")
                with gzip.open(save_path, "wt", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
                self.logger.info(f"PAGE SAVED TO 📁 :-{save_path}")

            except Exception as e:
                self.logger.error(f"PAGE SAVE ERROR: {e}")

        except Exception as e:
            self.logger.error(f"JSON LOAD ERROR: {e}")
            return

        # ── Base shortcuts ───────────────────────────────────────────────────
        resp = data.get("RESPONSE", {})
        print(resp.keys())
        page_context = resp.get("pageData", {}).get("pageContext", {})
        slots = resp.get("slots", [])
        slot_map = {s.get("id"): s for s in slots}  # {id: slot}
        psi = (page_context
               .get("fdpEventTracking", {})
               .get("events", {})
               .get("psi", {}))

        # helper: pull .value.text from a DLS label node, normalise list→str
        def t(node):
            if not isinstance(node, dict):
                return ""
            raw = node.get("value", {}).get("text", "")
            return ", ".join(str(x) for x in raw if str(x).strip()) if isinstance(raw, list) else str(raw).strip()

        # helper: safe slot DLS access
        def dls(slot_id):
            return slot_map.get(slot_id, {}).get("widget", {}).get("data", {}).get("dlsData", {})


        # =====================================================================
        # PRODUCT ID
        # =====================================================================
        product_id = page_context.get("productId", "")

        # =====================================================================
        # BRAND + PRODUCT NAME
        # Slot 14 (default_fk_pp_productTitle)
        #   label_3.value.text              → brand
        #   customEllipsisData_0.value
        #     .prependingText               → product title
        # =====================================================================
        brand = ""
        product_name = ""
        try:
            d14 = dls(14)
            brand = str(d14.get("label_3", {}).get("value", {}).get("text", "")).strip()
            product_name = str(d14.get("customEllipsisData_0", {}).get("value", {}).get("prependingText", "")).strip()
        except Exception as e:
            self.logger.warning(f"brand/title: {e}")

        # =====================================================================
        # PRICING
        # psi.ppd → mrp, fsp (selling price), nepPrice (best bank-offer price)
        # =====================================================================
        mrp = ""
        product_price = ""
        nep_price = ""
        discount = ""
        try:
            ppd = psi.get("ppd", {})
            mrp = ppd.get("mrp") or ppd.get("maximumRetailPrice") or ""
            product_price = ppd.get("fsp") or ppd.get("finalPrice") or ppd.get("searchPrice") or ""
            nep_price = ppd.get("nepPrice") or ""
            if mrp and product_price:
                discount = round(((float(mrp) - float(product_price)) / float(mrp)) * 100)
        except Exception as e:
            self.logger.warning(f"pricing: {e}")

        # =====================================================================
        # RATINGS
        # psi.pr → rating, ratingsCount, reviewsCount
        # =====================================================================
        avg_rating = ""
        number_of_ratings = ""
        number_of_reviews = ""
        try:
            pr = psi.get("pr", {})
            avg_rating = pr.get("rating", "")
            number_of_ratings = pr.get("ratingsCount", "")
            number_of_reviews = pr.get("reviewsCount", "")
        except Exception as e:
            self.logger.warning(f"ratings: {e}")

        # =====================================================================
        # AVAILABILITY / SHIPPING / RETURN
        # psi.pls → isAvailable, availabilityStatus
        # psi.pi  → isCODAvailable, returnPolicy
        # psi.sla → feeApplicable (0 = free), minSLA / maxSLA
        # =====================================================================
        is_sold_out = False
        cod_available = ""
        return_policy = ""
        shipping_charges = ""
        delivery_days = ""
        try:
            pls = psi.get("pls", {})
            pi = psi.get("pi", {})
            sla = psi.get("sla", [{}])
            sla = sla[0] if isinstance(sla, list) and sla else (sla if isinstance(sla, dict) else {})
            is_sold_out = not pls.get("isAvailable", True)
            cod_available = pi.get("isCODAvailable", "")
            return_policy = pi.get("returnPolicy", "")
            shipping_charges = sla.get("feeApplicable", "")  # 0 = free delivery
            delivery_days = sla.get("minSLA", "") or sla.get("maxSLA", "")
            days_match = re.search(r'\d+', str(delivery_days))
            days = int(days_match.group()) if days_match else 0

            # 2. Add the days to the current date using timedelta
            current_date = datetime.datetime.now()
            arrival_dt = current_date + timedelta(days=days)

            # 3. Format the date into 'yyyyddmm 00:00:00'
            # %Y = 4-digit year, %d = 2-digit day, %m = 2-digit month
            arrival_date = arrival_dt.strftime("%Y-%d-%m 00:00:00")
        except Exception as e:
            self.logger.warning(f"availability: {e}")

        # =====================================================================
        # CATEGORY HIERARCHY
        # Slot 6 multimedia rating overlay → box_1.action.tracking
        #   superCategory → l1, category → l2,
        #   subCategory   → l3, vertical  → l4
        # =====================================================================
        category_hierarchy = {"l1": "", "l2": "", "l3": "", "l4": ""}
        try:
            track = (dls(6)
                     .get("default_fk_pp_multimedia_rating_0", {})
                     .get("value", {})
                     .get("box_1", {})
                     .get("action", {})
                     .get("tracking", {}))
            category_hierarchy = {
                "l1": track.get("superCategory", ""),
                "l2": track.get("category", ""),
                "l3": track.get("subCategory", ""),
                "l4": track.get("vertical", ""),
            }
        except Exception as e:
            self.logger.warning(f"category: {e}")

        # =====================================================================
        # IMAGES
        # Slot 6 → multiMediaViewData_0 (list of media items)
        #   each item: image_0.value.selected.value.dynamicImageUrl
        # First unique URL → image_url (main); rest → extra_images
        # =====================================================================
        image_url = ""
        extra_images = []
        try:
            media_items = dls(6).get("multiMediaViewData_0", {}).get("value", [])
            seen_urls = []
            for item in media_items:
                url = (item.get("value", {})
                       .get("image_0", {})
                       .get("value", {})
                       .get("selected", {})
                       .get("value", {})
                       .get("dynamicImageUrl"))
                if url:
                    url = (url.replace("{@width}", "1080")
                           .replace("{@height}", "1080")
                           .replace("{@quality}", "100"))
                    if url not in seen_urls:
                        seen_urls.append(url)
            image_url = seen_urls[0] if seen_urls else ""
            extra_images = seen_urls[1:] if len(seen_urls) > 1 else []
        except Exception as e:
            self.logger.warning(f"images: {e}")

        # =====================================================================
        # HIGHLIGHTS  (Product highlights section)
        # Slot 30 (product-details-layout)
        #   product-details-grid_0.value.gridData_0.value[]
        #   each row: label_0 = key, label_1 = value
        # =====================================================================
        highlights = {}
        try:
            rows = (dls(30)
                    .get("product-details-grid_0", {})
                    .get("value", {})
                    .get("gridData_0", {})
                    .get("value", []))
            for row in rows:
                rv = row.get("value", {})
                key = t(rv.get("label_0", {}))
                val = t(rv.get("label_1", {}))
                if key and val:
                    highlights[key] = val
        except Exception as e:
            self.logger.warning(f"highlights: {e}")

        # =====================================================================
        # SPECIFICATIONS  (All details / Specifications tab)
        # Slot 32 → rpd_tab_showcase_vertical_list_0
        #   → rpd_specifications_grid_layout_1.value.gridData_0[]
        #     → rpd_grid_0.value.gridData_0[]
        #       each inner row: label_0 = spec key, label_2 = spec value
        # =====================================================================
        specifications = {}
        try:
            rpd = dls(32).get("rpd_tab_showcase_vertical_list_0", {}).get("value", {})
            outer = (rpd.get("rpd_specifications_grid_layout_1", {})
                     .get("value", {})
                     .get("gridData_0", {})
                     .get("value", []))
            for row in outer:
                inner = (row.get("value", {})
                         .get("rpd_grid_0", {})
                         .get("value", {})
                         .get("gridData_0", {})
                         .get("value", []))
                for ir in inner:
                    irv = ir.get("value", {})
                    key = t(irv.get("label_0", {}))
                    val = t(irv.get("label_2", {}))
                    if key and val:
                        specifications[key] = val
        except Exception as e:
            self.logger.warning(f"specifications: {e}")

            # =====================================================================
            # COLORS
            #
            # =====================================================================
        colors_variations = []
        try:
            col_items = (dls(8)
                          .get("variant-selector-image-view_0", {})
                          .get("value", {})
                          .get("horizontalListData_0", {})
                          .get("value", []))
            for si in col_items:
                track_si = si.get("value", {}).get("trackerData_0", {}).get("tracking", {})
                ct = track_si.get("contentType", "")
                name = track_si.get("contentTitle", "")
                var_id = track_si.get("productId")
                if var_id:
                    colors_variations.append(
                        var_id

                    )
        except Exception as e:
            self.logger.warning(f"sizes: {e}")

        # =====================================================================
        # SIZES
        # Slot 11 (size-selector-view-wrapper)
        #   size-selector-view_0.value.scrollToListData_0.value[]
        #   trackerData_0.tracking:
        #     contentTitle → size name
        #     contentType  → "InStock:Variant" | "OutOfStock:Variant" | "Scarcity:Variant"
        # =====================================================================
        sizes_variation = []
        try:
            size_items = (dls(11)
                          .get("size-selector-view_0", {})
                          .get("value", {})
                          .get("scrollToListData_0", {})
                          .get("value", []))
            for si in size_items:
                track_si = si.get("value", {}).get("trackerData_0", {}).get("tracking", {})
                ct = track_si.get("contentType", "")
                name = track_si.get("contentTitle", "")
                var_id=track_si.get("productId")
                if var_id:
                    sizes_variation.append(
                        var_id

                    )
        except Exception as e:
            self.logger.warning(f"sizes: {e}")

        # =====================================================================
        # BANK OFFERS
        # Slot id=19 (ATLAS_NEP_V2) → widget.data.offers[]
        #   → value.offerSummariesRC[] → value.bankOfferGrid[]
        #   each: value.offerTitle, value.discountedPriceText,
        #         tracking.contentTitle → "Bank_CardType • OfferType"
        # =====================================================================
        bank_offers = []

        try:

            slot19 = next((s for s in slots if s.get("id") == 19), {})
            offers_raw = slot19.get("widget", {}).get("data", {}).get("offers", [])
            for og in offers_raw:
                for summary in og.get("value", {}).get("offerSummariesRC", []):
                    for bg in summary.get("value", {}).get("bankOfferGrid", []):
                        bgv = bg.get("value", {})
                        ct = bg.get("tracking", {}).get("contentTitle", "")
                        parts = ct.split("_", 1)
                        bank_offers.append({
                            "bank": bgv.get("offerTitle", ""),
                            "discount": bgv.get("discountedPriceText", ""),
                            "type": parts[1] if len(parts) > 1 else "",
                        })
        except Exception as e:
            self.logger.warning(f"bank_offers: {e}")

        seller_name = ""
        seller_rating = ""

        try:
            seller_node = dls(24).get("default_fk_pp_delivery_widget_seller_2", {}).get("value", {})
            texts = []
            sellr_duration_on_flipkar = seller_node.get("label_3").get("value").get("text")

            def _collect(obj):
                if isinstance(obj, dict):
                    for k, v in obj.items():
                        if k == "text" and isinstance(v, str) and v.strip() not in ("", "•", " "):
                            texts.append(v.strip())
                        else:
                            _collect(v)
                elif isinstance(obj, list):
                    for x in obj:
                        _collect(x)

            _collect(seller_node)
            for tx in texts:
                if not seller_name and (tx.startswith("Fulfilled by") or tx.startswith("Sold by")):
                    seller_name = tx
                if not seller_rating and tx.replace(".", "").isdigit():
                    seller_rating = tx
        except Exception as e:
            self.logger.warning(f"seller: {e}")
        #ratings_count
        rate_list=page_context.get("fdpEventTracking").get("events").get("psi").get("pr",{}).get("individualRatingsCount",[])

        if rate_list:
            rate_data = {}
            for rate in rate_list:
                key=rate.get("ratingValue")
                val=rate.get("ratingCount")
                rate_data[key]=val
        else:
            rate_data=None

        description = ""
        features = []
        manufacturer_info = {}

        # ── Try slot 31 (Layout A) ───────────────────────────────────────────
        layout31 = (dls(31)
                    .get("rpd_tab_feature_descricption_manufacture_layout_1", {})
                    .get("value", {}))

        if layout31:
            # Description – label_1
            try:
                desc_raw = (layout31
                            .get("rpd_description_item_3", {})
                            .get("value", {})
                            .get("label_1", {})
                            .get("value", {})
                            .get("text", ""))
                description = str(desc_raw).strip()
            except Exception as e:
                self.logger.warning(f"description (slot31): {e}")

            # Features – carousel; modal DLS has label_0=title, label_1=body
            try:
                feat_carousel = (layout31
                                 .get("rpd_feature_layout_2", {})
                                 .get("value", {})
                                 .get("carouselData_0", {})
                                 .get("value", []))
                for fi in feat_carousel:
                    try:
                        modal_dls = (fi["value"]["row_0"]["action"]["params"]
                        ["widgetData"]["data"]["dlsData"])
                        title = modal_dls.get("label_0", {}).get("value", {}).get("text", "").strip()
                        body = modal_dls.get("label_1", {}).get("value", {}).get("text", "").strip()
                        if title or body:
                            features.append({"title": title, "description": body})
                    except Exception:
                        pass
            except Exception as e:
                self.logger.warning(f"features (slot31): {e}")

            # Manufacturer – same key in both layouts
            try:
                mfg_map = layout31.get("rpd_manufacture_layout_4", {}).get("value", {})
                for k, v in mfg_map.items():
                    if not k.startswith("default_fk_pp_rpd_header_body"):
                        continue
                    val = v.get("value", {})
                    field_name = val.get("label_0", {}).get("value", {}).get("text", "")
                    field_value = val.get("label_1", {}).get("value", {}).get("text", "")
                    if isinstance(field_value, list):
                        field_value = ", ".join(str(x) for x in field_value).strip()
                    else:
                        field_value = str(field_value).strip()
                    if field_name and field_value:
                        manufacturer_info[field_name] = field_value
            except Exception as e:
                self.logger.warning(f"manufacturer_info (slot31): {e}")

        # ── Fall back to slot 32 (Layout B) if slot 31 produced nothing ─────
        # (also runs if slot 31 exists but description/mfr came back empty)
        layout32 = (dls(32)
                    .get("rpd_tab_showcase_vertical_list_0", {})
                    .get("value", {}))

        if layout32:
            # Description – label_0  (key difference from Layout A)
            if not description:
                try:
                    desc_raw = (layout32
                                .get("rpd_description_item_3", {})
                                .get("value", {})
                                .get("label_0", {})
                                .get("value", {})
                                .get("text", ""))
                    description = str(desc_raw).strip()
                except Exception as e:
                    self.logger.warning(f"description (slot32): {e}")

            # Features – slot 32 doesn't carry inline feature text;
            # only a "Show More" navigation button is present, so we skip.

            # Manufacturer – same structure as Layout A
            if not manufacturer_info:
                try:
                    mfg_map = layout32.get("rpd_manufacture_layout_4", {}).get("value", {})
                    for k, v in mfg_map.items():
                        if not k.startswith("default_fk_pp_rpd_header_body"):
                            continue
                        val = v.get("value", {})
                        field_name = val.get("label_0", {}).get("value", {}).get("text", "")
                        field_value = val.get("label_1", {}).get("value", {}).get("text", "")
                        if isinstance(field_value, list):
                            field_value = ", ".join(str(x) for x in field_value).strip()
                        else:
                            field_value = str(field_value).strip()
                        if field_name and field_value:
                            manufacturer_info[field_name] = field_value
                except Exception as e:
                    self.logger.warning(f"manufacturer_info (slot32): {e}")

        others={
            "brand": brand,
            "images": extra_images,

            "highlights": highlights,
            "specifications": specifications,
            "description": description,  # ← ADD
            "features": features,  # ← ADD
            "manufacturer_info": manufacturer_info,  # ← ADD
            "colors_variation":colors_variations,
            "sizes_variations": sizes_variation,
            "bank_offer_price": nep_price,
            "bank_offers": bank_offers,
            "cod_available": cod_available,
            "return_policy": return_policy,
            "delivery_days": delivery_days,
            "serller_info": {"seller_name": seller_name,
                             "seller_rating": seller_rating,
                             "duration": sellr_duration_on_flipkar},
            "number_of_reviews": number_of_reviews,
            "zip_code":380016
        }
        print(others)
        if rate_data is not None:
            others["rating_count"]=rate_data

        item= {

            "product_id": prod_id,
            "catalog_id": prod_id,
            "catalog_name": product_name,
            "source": "Flipkart",
            # "scraped_date": datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            "product_name": product_name,
            "image_url": image_url,
            "category_hierarchy": json.dumps(category_hierarchy),
            "product_price": product_price,
            "arrival_date": arrival_date,
            "shipping_charges": shipping_charges,
            "is_sold_out": is_sold_out,
            "discount": discount,
            "mrp": mrp,
            "page_url": "N/A",
            "product_url":"https://www.flipkart.com"+ product_url,
            "number_of_ratings": number_of_ratings,
            "avg_rating": avg_rating,
            "position": "N/A",
            "country_code": "IN",
            "others":json.dumps(clean_empty(others))
        }
        yield item

    def errback_http(self, failure):

        self.logger.error(f"REQUEST FAILED : {failure}")

    if __name__ == "__main__":
        execute("scrapy crawl pdp ".split())