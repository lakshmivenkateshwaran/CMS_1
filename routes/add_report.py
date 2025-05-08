from fastapi import APIRouter, Depends, Query, HTTPException, Response
from fastapi.responses import JSONResponse
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from collections import defaultdict
from datetime import date
import json
import csv
import io
import os
from typing import Optional, List
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, date, timedelta
from databases.database import get_db
from services.addreport_services import get_filtered_data, get_date_range_from_type
from services.email_util import send_email_report
from models.chart_model import ChartType
from models.category_model import Category
from models.sub_category_model import SubCategory    
from models.product_model import Product
from models.manufacturer_model import Manufacturer
from models.crawl_websites import CrawlingWebsiteLog
from models.crawl_websites_model import CrawlingWebsite
from schemas.crawl_schema import WebsiteCrawlSummary
from schemas.addreport_schema import SaveReportView
from schemas.addreport_schema import ReportSummary
from models.cms_country import CMSCountry
from models.cms_accountcategory import CMSAccountsCategoryLinks
from models.cms_category import CMSCategory
from models.cms_subcategory import CMSSubCategory
from models.cms_brand import CMSManufacturerBrand
from models.cms_summaryproduct import CMSSummaryProduct
from models.cms_model import CMSSummaryProductModel
from models.crawl_websites_model import CrawlingWebsite
from models.cms_price import CMSCrawlingWebsiteProduct
from models.cms_pricehistory import CMSProductPriceHistory
from models.cms_crawlhistory import CMSCrawlingWebsiteProductsCrawlHistory
from models.cms_clientreports import CMSClientReport
from models.cms_cache import CMSCache
from models.cms_parameters import CMSMSTParameter
from models.cms_clientreportparameter import CMSClientReportParameter
from models.cms_description_split import CMSSummaryDescriptionSplit
from models.cms_description_split_desc_link import CMSSummaryDescriptionSplitDescriptionLink
from models.cms_description_split_product_link import CMSSummaryDescriptionSplitProductLink
from security.security import get_current_user_id


router = APIRouter()

# @router.get("/report-data")
# def get_report_data_all(
#     report_name: str = Query(None),
#     chart_type: str = Query(None),
#     category: str = Query(None),
#     subcategory: str = Query(None),
#     product: str = Query(None),
#     manufacturer: str = Query(None),
#     db: Session = Depends(get_db)
# ):
#     filters = {
#         "report_name": report_name,
#         "chart_type_id": chart_type,
#         "category": category,
#         "subcategory": subcategory,
#         "product": product,
#         "manufacturer": manufacturer
#     }
#     data = get_filtered_data(db, filters)
#     return {"data": data}

# #  Dropdown endpoints
# @router.get("/chart-types")
# def get_chart_types_dropdown(db: Session = Depends(get_db)):
#     return db.query(ChartType).all()

# @router.get("/categories")
# def get_categories_dropdown(db: Session = Depends(get_db)):
#     return db.query(Category).all()

# @router.get("/subcategories")
# def get_subcategories_dropdown(category_id: int, db: Session = Depends(get_db)):
#     return db.query(SubCategory).filter(SubCategory.category_id == category_id).all()

# @router.get("/products")
# def get_products_dropdown(subcategory_id: int, db: Session = Depends(get_db)):
#     return db.query(Product).filter(Product.subcategory_id == subcategory_id).all()

# @router.get("/manufacturers")
# def get_manufacturers_dropdown(product_id: int, db: Session = Depends(get_db)):
#     return db.query(Manufacturer).filter(Manufacturer.product_id == product_id).all()

# crawl website data 
@router.get("/website-crawled-summary", response_model=list[WebsiteCrawlSummary])
def get_today_website_crawled_summary(db: Session = Depends(get_db)):
    today_date = int(datetime.now().strftime("%Y%m%d"))

    results = (
        db.query(
            CrawlingWebsite.companyName.label("websiteName"),
            func.sum(CrawlingWebsiteLog.productsCrawled).label("totalProductsCrawled")
        )
        .join(CrawlingWebsiteLog, CrawlingWebsite.id == CrawlingWebsiteLog.websiteId)
        .filter(
            CrawlingWebsiteLog.dateCrawl == today_date,
            CrawlingWebsiteLog.deleted == 0,
            CrawlingWebsite.deleted == 0
        )
        .group_by(CrawlingWebsiteLog.websiteId)
        .order_by(func.sum(CrawlingWebsiteLog.productsCrawled).desc())
        .all()
    )

    return results

# Country Dropdown
@router.get("/dropdown/countries")
def get_countries(db: Session = Depends(get_db)):
    countries = db.query(CMSCountry).all()
    return [{"id": country.country_code, "name": country.country} for country in countries]

# Category Dropdown
@router.get("/dropdown/categories")
def get_categories(country_id: int, db: Session = Depends(get_db)):  
    # Step 1: Fetch the country from CMSCountry table using country_code
    country = db.query(CMSCountry).filter(CMSCountry.country_code == country_id).first()
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")

    # Step 2: Get categoryIds linked to this country from the accounts_category_links table
    category_links = db.query(CMSAccountsCategoryLinks)\
        .filter(CMSAccountsCategoryLinks.countryId == country_id)\
        .all()

    # Step 3: Fetch categories by categoryId from CMSCategory table
    category_ids = [link.categoryId for link in category_links]
    categories = db.query(CMSCategory).filter(CMSCategory.iCategoryCode.in_(category_ids)).all()

    # Return categories as string values (name)
    return [{"id": category.iCategoryCode, "name": category.sCategoryName} for category in categories]

# Subcategory Dropdown
@router.get("/dropdown/subcategories")
def get_subcategories(category_id: int, db: Session = Depends(get_db)):
    subcategories = db.query(CMSSubCategory).filter(CMSSubCategory.iCategoryCode == category_id).all()
    return [{"id": subcategory.iCatSubCode, "name": subcategory.sCatSubName} for subcategory in subcategories]

# Brand Dropdown (Corrected based on ManufacturerBrand and SummaryProduct)
@router.get("/dropdown/brands")
def get_brands(category_id: int, subcategory_id: int, db: Session = Depends(get_db)):
    # Fetching brands from ManufacturerBrand table, linked to category and subcategory via SummaryProduct
    brands = db.query(CMSManufacturerBrand).join(CMSSummaryProduct, CMSSummaryProduct.iProductBrandCode == CMSManufacturerBrand.iManBrandCode)\
                                         .filter(CMSSummaryProduct.iProductCategoryCode == category_id)\
                                         .filter(CMSSummaryProduct.iProductCatSubCode == subcategory_id)\
                                         .distinct().all()

    return [{"id": brand.iManBrandCode, "name": brand.sBrandName} for brand in brands]

# Model Dropdown type
@router.get("/dropdown/models")
def get_models(category_id: int, subcategory_id: int, brand_id: int, db: Session = Depends(get_db)):
    models = db.query(CMSSummaryProductModel).filter(CMSSummaryProductModel.iProductCategoryCode == category_id)\
                                            .filter(CMSSummaryProductModel.iProductCatSubCode == subcategory_id)\
                                            .filter(CMSSummaryProductModel.iProductBrandCode == brand_id).all()
    return [{"id": model.id, "model_no": model.sProductModelNo} for model in models]
# Model Dropdown field
@router.get("/dropdown/descriptions")
def get_descriptions(category_id: int, country_id: int, db: Session = Depends(get_db)):
    descriptions = db.query(CMSSummaryDescriptionSplit).filter(
        CMSSummaryDescriptionSplit.iCategoryCode == category_id,
        CMSSummaryDescriptionSplit.iCountryCode == country_id,
        CMSSummaryDescriptionSplit.deleted == 0
    ).all()

    return [{"id": desc.id, "name": desc.sDescriptionHeading} for desc in descriptions]

# Description Field Dropdown based on selected Description
@router.get("/dropdown/description-fields")
def get_description_fields(description_id: int, db: Session = Depends(get_db)):
    description_fields = db.query(CMSSummaryDescriptionSplitDescriptionLink).filter(
        CMSSummaryDescriptionSplitDescriptionLink.summaryDescriptionSplitId == description_id,
        CMSSummaryDescriptionSplitDescriptionLink.deleted == 0
    ).all()

    return [{"id": field.id, "name": field.descriptionField} for field in description_fields]

 
# Retailer Dropdown
@router.get("/dropdown/retailers")
def get_retailers(country_id: int, db: Session = Depends(get_db)):
    # Get retailers (company names) from CrawlingWebsite based on country code
    retailers = db.query(CrawlingWebsite).filter(
        CrawlingWebsite.countryCode == country_id
    ).all()

    return [{"id": r.id, "name": r.companyName} for r in retailers]


@router.get("/submit")
def get_price_by_names(
    country: str = Query(...),
    category: str = Query(...),
    subcategory: str = Query(...),
    brand: str = Query(...),
    model: str = Query(...),
    retailer: str = Query(...),
    start_date: str = Query(None, description="Start date in YYYY-MM-DD format"),
    end_date: str = Query(None, description="End date in YYYY-MM-DD format"),
    date_type: Optional[str] = Query(None, description="Optional date type: MTD, QTD, Q1, Q2, etc."),
    db: Session = Depends(get_db)
):
    # Step 1: Resolve names to codes
    country_obj = db.query(CMSCountry).filter(CMSCountry.country == country).first()
    category_obj = db.query(CMSCategory).filter(CMSCategory.sCategoryName == category).first()
    subcategory_obj = db.query(CMSSubCategory).filter(CMSSubCategory.sCatSubName == subcategory).first()
    brand_obj = db.query(CMSManufacturerBrand).filter(CMSManufacturerBrand.sBrandName == brand).first()
    retailer_obj = db.query(CrawlingWebsite).filter(CrawlingWebsite.companyName == retailer).first()

    if not all([country_obj, category_obj, subcategory_obj, brand_obj, retailer_obj]):
        raise HTTPException(status_code=404, detail="One or more values not found")

    # Step 2: Match summary_products using selected filters
    summary_product = (
        db.query(CMSSummaryProduct)
        .filter(CMSSummaryProduct.iProductCountryCode == country_obj.country_code)
        .filter(CMSSummaryProduct.iProductCategoryCode == category_obj.iCategoryCode)
        .filter(CMSSummaryProduct.iProductCatSubCode == subcategory_obj.iCatSubCode)
        .filter(CMSSummaryProduct.sProductModelNo == model)
        .filter(CMSSummaryProduct.iProductBrandCode == brand_obj.iManBrandCode)
        .first()
    )

    if not summary_product:
        return {
            "country": country,
            "category": category,
            "subcategory": subcategory,
            "brand": brand,
            "model": model,
            "retailer": retailer,
            "message": "Matching product not found in summary_products"
        }

    # Step 3: Use iProductCode to get products
    crawling_products = (
        db.query(CMSCrawlingWebsiteProduct)
        .filter(CMSCrawlingWebsiteProduct.systemProductId == summary_product.iProductCode)
        .filter(CMSCrawlingWebsiteProduct.crawlWebsiteId == retailer_obj.id)
        .filter(CMSCrawlingWebsiteProduct.isActive == 1)
        .all()
    )

    if not crawling_products:
        return {
            "country": country,
            "category": category,
            "subcategory": subcategory,
            "brand": brand,
            "model": model,
            "retailer": retailer,
            "message": "Product found in summary, but not in crawling website products"
        }
    
    # Special Case: If date_type is "current_day", return current price
    if date_type == "current_day":
        today_int = int(date.today().strftime("%Y%m%d"))
        crawl_histories = (
            db.query(CMSCrawlingWebsiteProductsCrawlHistory)
            .filter(CMSCrawlingWebsiteProductsCrawlHistory.crawlWebsiteId == retailer_obj.id)
            .filter(CMSCrawlingWebsiteProductsCrawlHistory.crawlDate == today_int)
            .filter(CMSCrawlingWebsiteProductsCrawlHistory.deleted == 0)
            .all()
        )
        valid_product_ids = set()

        for history in crawl_histories:
            serialized = history.searializeProductCodes
            for product in crawling_products:
                pid = product.id
                if f'i:{pid};' in serialized or f's:{len(str(pid))}:"{pid}"' in serialized:
                    valid_product_ids.add(pid)
        
        # Filter crawling_products to include only those in crawl history
        filtered_products = [p for p in crawling_products if p.id in valid_product_ids]

        if not filtered_products:
           return {
                "country": country,
                "category": category,
                "subcategory": subcategory,
                "brand": brand,
                "model": model,
                "retailer": retailer,
                "message": "No valid product found in crawl history for current day"
            }
        return [
           {
            "country": country,
            "category": category,
            "subcategory": subcategory,
            "brand": brand,
            "model": model,
            "retailer": retailer,
            "price": f"${product.price:,.2f}" if product.price else "N/A",
           }

           for product in filtered_products
        ]
        
    # Step 4: Handle date filters
    if start_date and end_date:
       try:
           start_dt = datetime.strptime(start_date, "%Y-%m-%d")
           end_dt = datetime.strptime(end_date, "%Y-%m-%d")
           start = int(start_dt.strftime("%Y%m%d"))
           end = int(end_dt.strftime("%Y%m%d"))
       except ValueError:
             raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
    elif date_type:
        start_dt, end_dt = get_date_range_from_type(date_type)
        if not start_dt or not end_dt:
           raise HTTPException(status_code=400, detail="Invalid date_type value")
        start = int(start_dt.strftime("%Y%m%d"))
        end = int(end_dt.strftime("%Y%m%d"))
    else:
        raise HTTPException(status_code=400, detail="Please provide a date range or date_type to fetch price history")

    # Step 5: Match product IDs with crawl history via serialized codes
    crawl_histories = (
        db.query(CMSCrawlingWebsiteProductsCrawlHistory)
        .filter(CMSCrawlingWebsiteProductsCrawlHistory.crawlWebsiteId == retailer_obj.id)
        .filter(CMSCrawlingWebsiteProductsCrawlHistory.deleted == 0)
        .all()
    )

    matched_entries = defaultdict(list)

    # Group crawl records by crawlDate where a match with product ID exists
    for history in crawl_histories:
        serialized = history.searializeProductCodes
        for product in crawling_products:
            pid = product.id
            if f'i:{pid};' in serialized or f's:{len(str(pid))}:"{pid}"' in serialized:
                if start <= history.crawlDate <= end:
                    matched_entries[history.crawlDate].append({
                        "product_id": pid,
                        "crawl_date": history.crawlDate,
                        "created_at": history.created
                    })
    
    # Now you need to process each crawlDate and select the latest record for each one
    final_matched_entries = []

    # For each crawlDate, pick the record with latest created_at
    for crawl_date, records in matched_entries.items():
         latest_record = max(records, key=lambda x: x["created_at"])

         # Add the latest record to final list
         final_matched_entries.append({
             "product_id": latest_record["product_id"],
             "crawl_date": latest_record["crawl_date"]
        })

    if not matched_entries:
        return {
            "country": country,
            "category": category,
            "subcategory": subcategory,
            "brand": brand,
            "model": model,
            "retailer": retailer,
            "message": "No matching crawl history data found for the given products and date range"
        }

    # Step 6: Get all matched product IDs and latest created crawlDate per product
    product_latest_crawl = {}

    for record in final_matched_entries:
        pid = record["product_id"]
        crawl_date = record["crawl_date"]
        if pid not in product_latest_crawl or product_latest_crawl[pid]["created_at"] < record.get("created_at", datetime.min):
            product_latest_crawl[pid] = {
                "crawl_date": crawl_date,
                "created_at": record.get("created_at", datetime.min)
            }

    # Step 7: Get latest price history reference date per product
    latest_price_history = (
        db.query(CMSProductPriceHistory.productId, func.max(CMSProductPriceHistory.referenceDate).label("last_ref"))
        .filter(CMSProductPriceHistory.productId.in_(product_latest_crawl.keys()))
        .filter(CMSProductPriceHistory.crawlWebsiteId == retailer_obj.id)
        .filter(CMSProductPriceHistory.deleted == 0)
        .group_by(CMSProductPriceHistory.productId)
        .all()
    )

    product_last_ref_date = {
        p.productId: p.last_ref for p in latest_price_history
    }

    # Load full history for all matched products
    full_history_prices = defaultdict(dict)

    history_records = (
        db.query(CMSProductPriceHistory)
        .filter(CMSProductPriceHistory.productId.in_(product_latest_crawl.keys()))
        .filter(CMSProductPriceHistory.crawlWebsiteId == retailer_obj.id)
        .filter(CMSProductPriceHistory.deleted == 0)
        .all()
    )

    for record in history_records:
        full_history_prices[record.productId][record.referenceDate] = record.price


    # Step 8: Get crawling website product prices (used for forward fill)
    product_prices = {
        p.id: p.price for p in crawling_products if p.price is not None
    }

    # Step 9: Build complete timeline
    final_result = []
    all_dates = []
    cursor = start_dt.date()
    while cursor <= end_dt.date():
        all_dates.append(cursor)
        cursor += timedelta(days=1)
    
    today_date = date.today()
    for pid in product_latest_crawl.keys():
        crawl_date = product_latest_crawl[pid]["crawl_date"]
        forward_price = product_prices.get(pid)
        history_map = full_history_prices.get(pid, {})

        last_history_date = max(history_map.keys()) if history_map else None
        last_history_price = history_map.get(last_history_date) if last_history_date else None

        for date_obj in all_dates:
            if date_obj > today_date:
                continue  # Skip dates in the future
            date_int = int(date_obj.strftime("%Y%m%d"))
            display_date = date_obj.strftime("%d-%m-%Y")

            if date_int == last_history_date:
                # Replace last historical date with crawling website price if available
                if forward_price is not None:
                    final_result.append({
                        "country": country,
                        "category": category,
                        "subcategory": subcategory,
                        "brand": brand,
                        "model": model,
                        "retailer": retailer,
                        "Date": display_date,
                        "price": f"${forward_price:,.2f}"
                    })

            elif date_int in history_map:
                # Other historical dates
                price = history_map[date_int]
                final_result.append({
                    "country": country,
                    "category": category,
                    "subcategory": subcategory,
                    "brand": brand,
                    "model": model,
                    "retailer": retailer,
                    "Date": display_date,
                    "price": f"${price:,.2f}"
                })

            elif last_history_date and date_int < last_history_date:
                # Backfill using last known historical price
                if last_history_price is not None:
                    final_result.append({
                        "country": country,
                        "category": category,
                        "subcategory": subcategory,
                        "brand": brand,
                        "model": model,
                        "retailer": retailer,
                        "Date": display_date,
                        "price": f"${last_history_price:,.2f}"
                    })
                    
            elif crawl_date and date_int >= crawl_date and forward_price is not None:
                # Forward fill using crawling website price
                final_result.append({
                    "country": country,
                    "category": category,
                    "subcategory": subcategory,
                    "brand": brand,
                    "model": model,
                    "retailer": retailer,
                    "Date": display_date,
                    "price": f"${forward_price:,.2f}"
                })

    return final_result



    
@router.get("/export-excel")
def export_selected_data_as_excel(
    country: str = Query(...),
    category: str = Query(...),
    subcategory: str = Query(...),
    brand: str = Query(...),
    model: str = Query(...),
    retailer: str = Query(...),
    start_date: Optional[str] = Query(None, description="Start date in YYYY-MM-DD format"),
    end_date: Optional[str] = Query(None, description="End date in YYYY-MM-DD format"),
    date_type: Optional[str] = Query(None, description="Choose from QTD, MTD, Last Month, etc."),
    db: Session = Depends(get_db)
):
    # Step 1: Resolve necessary objects
    country_obj = db.query(CMSCountry).filter(CMSCountry.country == country).first()
    retailer_obj = db.query(CrawlingWebsite).filter(CrawlingWebsite.companyName == retailer).first()

    if not country_obj or not retailer_obj:
        raise HTTPException(status_code=404, detail="Country or Retailer not found")

    # Step 2: Resolve product summary
    summary_product = (
        db.query(CMSSummaryProduct)
        .join(CMSCategory, CMSSummaryProduct.iProductCategoryCode == CMSCategory.iCategoryCode)
        .join(CMSSubCategory, CMSSummaryProduct.iProductCatSubCode == CMSSubCategory.iCatSubCode)
        .join(CMSManufacturerBrand, CMSSummaryProduct.iProductBrandCode == CMSManufacturerBrand.iManBrandCode)
        .filter(CMSSummaryProduct.sProductModelNo == model)
        .filter(CMSCategory.sCategoryName == category)
        .filter(CMSSubCategory.sCatSubName == subcategory)
        .filter(CMSManufacturerBrand.sBrandName == brand)
        .filter(CMSSummaryProduct.iProductCountryCode == country_obj.country_code)
        .first()
    )

    if not summary_product:
        raise HTTPException(status_code=404, detail="No matching product found in summary table")

    # Step 3: Get all matching products
    products = (
        db.query(CMSCrawlingWebsiteProduct)
        .filter(CMSCrawlingWebsiteProduct.systemProductId == CMSSummaryProduct.iProductCode)
        .filter(CMSCrawlingWebsiteProduct.crawlWebsiteId == retailer_obj.id)
        .filter(CMSCrawlingWebsiteProduct.isActive == 1)
        .all()
    )

    if not products:
        raise HTTPException(status_code=404, detail="No active product found to export")

    # Excel setup
    wb = Workbook()
    ws = wb.active
    ws.title = "Report"

    # Header & Styles
    if start_date and end_date or date_type:
        headers = ["Country", "Category", "Subcategory", "Brand", "Model", "Retailer", "Price", "Reference Date"]
    else:
        headers = ["Country", "Category", "Subcategory", "Brand", "Model", "Retailer", "Price"]

    ws.append(headers)
    header_fill = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")
    for cell in ws[1]:
        cell.font = Font(bold=True)
        cell.fill = header_fill

    # Handle date type if provided
    if date_type and not (start_date and end_date):
        start_dt, end_dt = get_date_range_from_type(date_type)
        if not start_dt or not end_dt:
            raise HTTPException(status_code=400, detail="Invalid date_type provided.")
        start_date = start_dt.strftime("%Y-%m-%d")
        end_date = end_dt.strftime("%Y-%m-%d")

    elif date_type and (start_date or end_date):
        raise HTTPException(status_code=400, detail="Provide either date_type OR start_date/end_date — not both.")

    # Step 4: Fetch price history if date filters applied
    if start_date and end_date:
        try:
            start = int(datetime.strptime(start_date, "%Y-%m-%d").strftime("%Y%m%d"))
            end = int(datetime.strptime(end_date, "%Y-%m-%d").strftime("%Y%m%d"))
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

        product_ids = [p.id for p in products]

        history_prices = (
            db.query(CMSProductPriceHistory)
            .filter(CMSProductPriceHistory.productId.in_(product_ids))
            .filter(CMSProductPriceHistory.crawlWebsiteId == retailer_obj.id)
            .filter(CMSProductPriceHistory.referenceDate.between(start, end))
            .filter(CMSProductPriceHistory.deleted == 0)
            .all()
        )

        for p in history_prices:
            ws.append([
                country, category, subcategory, brand, model, retailer, f"${p.price:,.2f}", datetime.strptime(str(p.referenceDate), "%Y%m%d").strftime("%d-%m-%Y")
            ])

        if not history_prices:
            ws.append([
                country, category, subcategory, brand, model, retailer, "N/A",
                f"No price history found between {start_date} and {end_date}"
            ])
    else:
        for product in products:
            ws.append([
                country, category, subcategory, brand, model, retailer, f"${product.price:,.2f}"
            ])

    # Save Excel to memory stream
    stream = io.BytesIO()
    wb.save(stream)
    stream.seek(0)

    return Response(
        content=stream.read(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={brand}_Report.xlsx"}
    )
    
@router.get("/export-csv")
def export_selected_data_as_csv(
    country: str = Query(...),
    category: str = Query(...),
    subcategory: str = Query(...),
    brand: str = Query(...),
    model: str = Query(...),
    retailer: str = Query(...),
    start_date: str = Query(None, description="Start date in YYYY-MM-DD format"),
    end_date: str = Query(None, description="End date in YYYY-MM-DD format"),
    date_type: str = Query(None, description="Choose from QTD, MTD, Last Month, etc."),
    db: Session = Depends(get_db)
):
    # Step 1: Resolve necessary names to objects
    country_obj = db.query(CMSCountry).filter(CMSCountry.country == country).first()
    retailer_obj = db.query(CrawlingWebsite).filter(CrawlingWebsite.companyName == retailer).first()

    if not country_obj or not retailer_obj:
        raise HTTPException(status_code=404, detail="Country or Retailer not found")

    # Step 2: Resolve product from summary
    summary_product = (
        db.query(CMSSummaryProduct)
        .join(CMSCategory, CMSSummaryProduct.iProductCategoryCode == CMSCategory.iCategoryCode)
        .join(CMSSubCategory, CMSSummaryProduct.iProductCatSubCode == CMSSubCategory.iCatSubCode)
        .join(CMSManufacturerBrand, CMSSummaryProduct.iProductBrandCode == CMSManufacturerBrand.iManBrandCode)
        .filter(CMSSummaryProduct.sProductModelNo == model)
        .filter(CMSCategory.sCategoryName == category)
        .filter(CMSSubCategory.sCatSubName == subcategory)
        .filter(CMSManufacturerBrand.sBrandName == brand)
        .filter(CMSSummaryProduct.iProductCountryCode == country_obj.country_code)
        .first()
    )

    if not summary_product:
        raise HTTPException(status_code=404, detail="No matching product found in summary table")

    # Step 3: Get all matching products from crawling_website_products
    products = (
        db.query(CMSCrawlingWebsiteProduct)
        .filter(CMSCrawlingWebsiteProduct.systemProductId == CMSSummaryProduct.iProductCode)
        .filter(CMSCrawlingWebsiteProduct.crawlWebsiteId == retailer_obj.id)
        .filter(CMSCrawlingWebsiteProduct.isActive == 1)
        .all()
    )

    if not products:
        raise HTTPException(status_code=404, detail="No active product found to export")

    output = io.StringIO()

    # Date type handling
    if date_type and not (start_date and end_date):
        start_dt, end_dt = get_date_range_from_type(date_type)
        if not start_dt or not end_dt:
            raise HTTPException(status_code=400, detail="Invalid date_type provided.")
        start_date = start_dt.strftime("%Y-%m-%d")
        end_date = end_dt.strftime("%Y-%m-%d")

    elif date_type and (start_date or end_date):
        raise HTTPException(status_code=400, detail="Provide either date_type OR start_date/end_date — not both.")

    # Step 4: If date filters are provided, fetch price history
    if start_date and end_date:
        try:
            start = int(datetime.strptime(start_date, "%Y-%m-%d").strftime("%Y%m%d"))
            end = int(datetime.strptime(end_date, "%Y-%m-%d").strftime("%Y%m%d"))
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

        product_ids = [p.id for p in products]

        history_prices = (
            db.query(CMSProductPriceHistory)
            .filter(CMSProductPriceHistory.productId.in_(product_ids))
            .filter(CMSProductPriceHistory.crawlWebsiteId == retailer_obj.id)
            .filter(CMSProductPriceHistory.referenceDate.between(start, end))
            .filter(CMSProductPriceHistory.deleted == 0)
            .all()
        )

        fieldnames = ["Country", "Category", "Subcategory", "Brand", "Model", "Retailer", "Price", "Reference Date"]
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()

        for p in history_prices:
            writer.writerow({
                "Country": country,
                "Category": category,
                "Subcategory": subcategory,
                "Brand": brand,
                "Model": model,
                "Retailer": retailer,
                "Price": f"${p.price:,.2f}",
                "Reference Date": datetime.strptime(str(p.referenceDate), "%Y%m%d").strftime("%d-%m-%Y")
            })

        if not history_prices:
            writer.writerow({
                "Country": country,
                "Category": category,
                "Subcategory": subcategory,
                "Brand": brand,
                "Model": model,
                "Retailer": retailer,
                "Price": "N/A",
                "Reference Date": f"No price history found between {start_date} and {end_date}"
            })

    else:
        # Step 5: Default to current product price export
        fieldnames = ["Country", "Category", "Subcategory", "Brand", "Model", "Retailer", "Price"]
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()

        for product in products:
            writer.writerow({
                "Country": country,
                "Category": category,
                "Subcategory": subcategory,
                "Brand": brand,
                "Model": model,
                "Retailer": retailer,
                "Price": f"${product.price:,.2f}"
            })

    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={brand}_Report.csv"}
    )

@router.get("/export-pdf")
def export_selected_data_as_pdf(
    country: str = Query(...),
    category: str = Query(...),
    subcategory: str = Query(...),
    brand: str = Query(...),
    model: str = Query(...),
    retailer: str = Query(...),
    start_date: str = Query(None, description="Start date in YYYY-MM-DD format"),
    end_date: str = Query(None, description="End date in YYYY-MM-DD format"),
    date_type: str = Query(None, description="Choose from QTD, MTD, Last Month, etc."),
    db: Session = Depends(get_db)
):
    country_obj = db.query(CMSCountry).filter(CMSCountry.country == country).first()
    retailer_obj = db.query(CrawlingWebsite).filter(CrawlingWebsite.companyName == retailer).first()

    if not country_obj or not retailer_obj:
        raise HTTPException(status_code=404, detail="Country or Retailer not found")

    summary_product = (
        db.query(CMSSummaryProduct)
        .join(CMSCategory, CMSSummaryProduct.iProductCategoryCode == CMSCategory.iCategoryCode)
        .join(CMSSubCategory, CMSSummaryProduct.iProductCatSubCode == CMSSubCategory.iCatSubCode)
        .join(CMSManufacturerBrand, CMSSummaryProduct.iProductBrandCode == CMSManufacturerBrand.iManBrandCode)
        .filter(CMSSummaryProduct.sProductModelNo == model)
        .filter(CMSCategory.sCategoryName == category)
        .filter(CMSSubCategory.sCatSubName == subcategory)
        .filter(CMSManufacturerBrand.sBrandName == brand)
        .filter(CMSSummaryProduct.iProductCountryCode == country_obj.country_code)
        .first()
    )

    if not summary_product:
        raise HTTPException(status_code=404, detail="No matching product found in summary table")

    products = (
        db.query(CMSCrawlingWebsiteProduct)
        .filter(CMSCrawlingWebsiteProduct.systemProductId == CMSSummaryProduct.iProductCode)
        .filter(CMSCrawlingWebsiteProduct.crawlWebsiteId == retailer_obj.id)
        .filter(CMSCrawlingWebsiteProduct.isActive == 1)
        .all()
    )

    if not products:
        raise HTTPException(status_code=404, detail="No active product found to export")

    # Handle date_type logic
    if date_type and not (start_date and end_date):
        start_dt, end_dt = get_date_range_from_type(date_type)
        if not start_dt or not end_dt:
            raise HTTPException(status_code=400, detail="Invalid date_type provided.")
        start_date = start_dt.strftime("%Y-%m-%d")
        end_date = end_dt.strftime("%Y-%m-%d")

    elif date_type and (start_date or end_date):
        raise HTTPException(status_code=400, detail="Provide either date_type OR start_date/end_date — not both.")

    table_data = []
    report_title = ""
    if start_date and end_date:
        # Exporting price history
        try:
            start = int(datetime.strptime(start_date, "%Y-%m-%d").strftime("%Y%m%d"))
            end = int(datetime.strptime(end_date, "%Y-%m-%d").strftime("%Y%m%d"))
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

        product_ids = [p.id for p in products]
        history_prices = (
            db.query(CMSProductPriceHistory)
            .filter(CMSProductPriceHistory.productId.in_(product_ids))
            .filter(CMSProductPriceHistory.crawlWebsiteId == retailer_obj.id)
            .filter(CMSProductPriceHistory.referenceDate.between(start, end))
            .filter(CMSProductPriceHistory.deleted == 0)
            .all()
        )

        table_data = [["Country", "Category", "Subcategory", "Brand", "Model", "Retailer", "Reference Date", "Price"]]
        for p in history_prices:
            table_data.append([
                country,
                category,
                subcategory,
                brand,
                model,
                retailer,
                datetime.strptime(str(p.referenceDate), "%Y%m%d").strftime("%d-%m-%Y"),
                f"${p.price:,.2f}"
            ])
        if not history_prices:
            table_data.append([
                country, category, subcategory, brand, model, retailer,
                f"No price history found between {start_date} and {end_date}",
                "N/A"
            ])
        report_title = f"{date_type or 'Date Range'}: {start_date} to {end_date}"

    else:
        # Exporting current prices
        table_data = [["Country", "Category", "Subcategory", "Brand", "Model", "Retailer", "Price"]]
        for product in products:
            table_data.append([
                country,
                category,
                subcategory,
                brand,
                model,
                retailer,
                f"${product.price:,.2f}"
            ])
        report_title = "Current Product Prices"

    # Generate PDF
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # CMS logo
    try:
       logo_path = r"C:\Users\venki\Work\cms_1\static\cms_logo.png"
       print("Logo exists:", os.path.exists(logo_path))  

    # Draw the image
       pdf.drawImage(logo_path, 1.5 * cm, height - 4 * cm, width=3 * cm, preserveAspectRatio=True)
    except Exception as e:
        print("Logo drawing failed:", e)
    

    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawCentredString(width / 2, height - 2.0 * cm, "Product Report")
    pdf.setFont("Helvetica", 12)
    pdf.drawCentredString(width / 2, height - 3.0 * cm, report_title)
    
    # Watermark: CMS
    pdf.saveState()
    pdf.setFont("Helvetica-Bold", 60)
    pdf.setFillColorRGB(0.85, 0.85, 0.85)  # light grey
    pdf.translate(width / 2, height / 2)
    pdf.rotate(45)  # Rotate text 45 degrees
    pdf.drawCentredString(0, 0, "CMS")
    pdf.restoreState()   

    # Draw table
    col_width = (width - 3 * cm) / len(table_data[0])
    table = Table(table_data, colWidths=[col_width] * len(table_data[0]))
    table.setStyle(TableStyle([  
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#d3d3d3")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5)
    ]))

    table.wrapOn(pdf, 2 * cm, 5 * cm)
    table.drawOn(pdf, 1.5 * cm, height - 8 * cm - len(table_data) * 12)

    pdf.save()
    buffer.seek(0)

    return Response(
        content=buffer.getvalue(),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={brand}_Report.pdf"}
    )

# Save the view in History section
@router.post("/report/save")
def save_report_view(
    payload: SaveReportView,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    # Step 1: Save report name in client_reports
    new_report = CMSClientReport(
        userId=user_id,
        clientId=payload.client_id,
        name=payload.report_name,
        worksheetPrefix="",
        reportGraphTypeId=1,
        reportTypeId=1,
        preGenerate='excel',
        created=datetime.now(),
        modified=datetime.now()
    )
    db.add(new_report)
    db.commit()
    db.refresh(new_report)

    # Step 1: Resolve names to codes
    country_obj = db.query(CMSCountry).filter(CMSCountry.country == payload.country).first()
    category_obj = db.query(CMSCategory).filter(CMSCategory.sCategoryName == payload.category).first()
    subcategory_obj = db.query(CMSSubCategory).filter(CMSSubCategory.sCatSubName == payload.subcategory).first()
    brand_obj = db.query(CMSManufacturerBrand).filter(CMSManufacturerBrand.sBrandName == payload.brand).first()
    model_obj = db.query(CMSSummaryProductModel).filter(CMSSummaryProductModel.sProductModelNo == payload.model).first()
    retailer_obj = db.query(CrawlingWebsite).filter(CrawlingWebsite.companyName == payload.retailer).first()

    if not all([country_obj, category_obj, subcategory_obj, brand_obj, retailer_obj, model_obj]):
        raise HTTPException(status_code=404, detail="One or more values not found")
    
    # Create JSON with IDs
    filters_as_ids = {
        "country_code": country_obj.country_code,
        "category_code": category_obj.iCategoryCode,
        "subcategory_code": subcategory_obj.iCatSubCode,
        "brand_code": brand_obj.iManBrandCode,
        "model": model_obj.id,
        "retailer_id": retailer_obj.id,
        "model": model_obj.id,
        "start_date": payload.start_date,
        "end_date": payload.end_date,
        "date_type": payload.date_type
    }

    cache_entry = CMSCache(
        reportId=new_report.id,
        keyDetails="Saved filter metadata",  # placeholder string
        keyContents=json.dumps(filters_as_ids),
        data="{}",                           # empty object or actual data if you want to store it
        adCountData="{}",                   # placeholder
        fileGenerated="",                   # assume not generated yet
        lastCalculateDate=int(datetime.now().strftime("%Y%m%d")),
        deleted=0
    )

    db.add(cache_entry)

    # Step 4: Save filters into cms_client_reports_parameters using mst_parameter
    filter_map = {
        "country": country_obj.country_code,
        "category": category_obj.iCategoryCode,
        "subcategory": subcategory_obj.iCatSubCode,
        "brand": brand_obj.iManBrandCode,
        "model": model_obj.id,
        "retailer": retailer_obj.id,
        "model": model_obj.id,
        "start_date": payload.start_date,
        "end_date": payload.end_date,
        "date_type": payload.date_type
    }

    for key, value in filter_map.items():
        if value is not None:
            param = db.query(CMSMSTParameter).filter(CMSMSTParameter.code == key).first()
            if param:
                param_entry = CMSClientReportParameter(
                    reportId=new_report.id,
                    parameterId=param.id,
                    value=str(value)
                )
                db.add(param_entry)
    db.commit()

    return {"message": "Report view and filters saved", "report_id": new_report.id}

# Saved reports summary 
@router.get("/report-views", response_model=List[ReportSummary])
def get_report_views(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    reports = db.query(CMSClientReport).filter(CMSClientReport.userId == user_id).order_by(CMSClientReport.created.desc()).all()
    return reports

# View action 
@router.get("/report/view/{report_id}")
def view_saved_report(report_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    # Step 1: Fetch the report
    report = db.query(CMSClientReport).filter(
        CMSClientReport.id == report_id, CMSClientReport.userId == user_id
    ).first()

    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    # Step 2: Get the latest cache data
    cache = (
        db.query(CMSCache)
        .filter(CMSCache.reportId == report_id)
        .order_by(CMSCache.id.desc())
        .first()
    )
    if not cache:
        raise HTTPException(status_code=404, detail="No cached data found for this report")

    filters = json.loads(cache.keyContents)

    # Step 3: Optionally, fetch readable names for display (optional)
    country = db.query(CMSCountry).filter(CMSCountry.country_code == filters.get("country_code")).first()
    category = db.query(CMSCategory).filter(CMSCategory.iCategoryCode == filters.get("category_code")).first()
    subcategory = db.query(CMSSubCategory).filter(CMSSubCategory.iCatSubCode == filters.get("subcategory_code"),CMSSubCategory.iCategoryCode == filters.get("category_code")).first()    
    brand = db.query(CMSManufacturerBrand).filter(CMSManufacturerBrand.iManBrandCode == filters.get("brand_code")).first()
    model = db.query(CMSSummaryProductModel).filter(CMSSummaryProductModel.id == filters.get("model")).first()
    retailer = db.query(CrawlingWebsite).filter(CrawlingWebsite.id == filters.get("retailer_id")).first()

    readable_filters = {
        "Country": country.country if country else "",
        "Category": category.sCategoryName if category else "",
        "Subcategory": subcategory.sCatSubName if subcategory else "",
        "Brand": brand.sBrandName if brand else "",
        "Retailer": retailer.companyName if retailer else "",
        "Model": model.sProductModelNo if model else "",
        "Start Date": filters.get("start_date"),
        "End Date": filters.get("end_date"),
        "Date Type": filters.get("date_type")
    }

    # Step 4: Return viewable data (or redirect to download endpoint)
    return JSONResponse({
        "report_id": report.id,
        "report_name": report.name,
        "filters": readable_filters,
        "data": cache.keyContents  
    })


# Get the saved report for update
@router.get("/report/edit/{report_id}")
def get_saved_report(report_id: int, db: Session = Depends(get_db)):
    # Step 1: Fetch the report
    report = db.query(CMSClientReport).filter(CMSClientReport.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    # Step 2: Get the associated cache entry (assuming 1-to-1 latest entry)
    cache = (
        db.query(CMSCache)
        .filter(CMSCache.reportId == report_id)
        .order_by(CMSCache.id.desc())  # just in case multiple entries exist
        .first()
    )

    if not cache:
        raise HTTPException(status_code=404, detail="Cache not found for this report")

    filters_json = json.loads(cache.keyContents)

    # Step 3: Resolve dropdown values from codes
    country = db.query(CMSCountry).filter(CMSCountry.country_code == filters_json.get("country_code")).first()
    category = db.query(CMSCategory).filter(CMSCategory.iCategoryCode == filters_json.get("category_code")).first()
    subcategory = db.query(CMSSubCategory).filter(CMSSubCategory.iCatSubCode == filters_json.get("subcategory_code"),CMSSubCategory.iCategoryCode == filters_json.get("category_code")).first()    
    brand = db.query(CMSManufacturerBrand).filter(CMSManufacturerBrand.iManBrandCode == filters_json.get("brand_code")).first()
    model = db.query(CMSSummaryProductModel).filter(CMSSummaryProductModel.id == filters_json.get("model")).first()
    retailer = db.query(CrawlingWebsite).filter(CrawlingWebsite.id == filters_json.get("retailer_id")).first()

    return {
        "report_id": report.id,
        "report_name": report.name,
        "filters": {
            "country": [{"id": country.country_code, "name": country.country}] if country else [],
            "category": [{"id": category.iCategoryCode, "name": category.sCategoryName}] if category else [],
            "subCategory": [{"id": subcategory.iCatSubCode, "name": subcategory.sCatSubName}] if subcategory else [],
            "retailer": [{"id": retailer.id, "name": retailer.companyName}] if retailer else [],
            "brand": [{"id": brand.iManBrandCode, "name": brand.sBrandName}] if brand else [],
            "model": [{"id": model.id, "name": model.sProductModelNo}] if model else [],
            "start_date": filters_json.get("start_date"),
            "end_date": filters_json.get("end_date"),
            "date_type": filters_json.get("date_type"),
        }
    }

# Updating the selected fields
@router.put("/report/update/{report_id}")
def update_report_view(
    report_id: int,
    payload: SaveReportView,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    # Step 1: Fetch and validate the report
    report = db.query(CMSClientReport).filter(
        CMSClientReport.id == report_id, CMSClientReport.userId == user_id
    ).first()

    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    # Step 2: Resolve names to codes
    country_obj = db.query(CMSCountry).filter(CMSCountry.country == payload.country).first()
    category_obj = db.query(CMSCategory).filter(CMSCategory.sCategoryName == payload.category).first()
    subcategory_obj = db.query(CMSSubCategory).filter(
        CMSSubCategory.sCatSubName == payload.subcategory,
        CMSSubCategory.iCategoryCode == category_obj.iCategoryCode
    ).first()
    brand_obj = db.query(CMSManufacturerBrand).filter(CMSManufacturerBrand.sBrandName == payload.brand).first()
    model_obj = db.query(CMSSummaryProductModel).filter(CMSSummaryProductModel.sProductModelNo == payload.model).first()
    retailer_obj = db.query(CrawlingWebsite).filter(CrawlingWebsite.companyName == payload.retailer).first()

    if not all([country_obj, category_obj, subcategory_obj, brand_obj, model_obj, retailer_obj]):
        raise HTTPException(status_code=404, detail="One or more values not found")

    # Step 3: Update `client_reports`
    report.name = payload.report_name
    report.modified = datetime.now()

    # Step 4: Update latest `cache` entry
    filters_as_ids = {
        "country_code": country_obj.country_code,
        "category_code": category_obj.iCategoryCode,
        "subcategory_code": subcategory_obj.iCatSubCode,
        "brand_code": brand_obj.iManBrandCode,
        "model": model_obj.id,
        "retailer_id": retailer_obj.id,
        "start_date": payload.start_date,
        "end_date": payload.end_date,
        "date_type": payload.date_type
    }

    latest_cache = (
        db.query(CMSCache)
        .filter(CMSCache.reportId == report_id)
        .order_by(CMSCache.id.desc())
        .first()
    )

    if latest_cache:
        latest_cache.keyContents = json.dumps(filters_as_ids)
        latest_cache.lastCalculateDate = int(datetime.now().strftime("%Y%m%d"))

    # Step 5: Clear old parameters and insert new ones
    db.query(CMSClientReportParameter).filter(CMSClientReportParameter.reportId == report_id).delete()

    filter_map = {
        "country": country_obj.country_code,
        "category": category_obj.iCategoryCode,
        "subcategory": subcategory_obj.iCatSubCode,
        "brand": brand_obj.iManBrandCode,
        "model": model_obj.id,
        "retailer": retailer_obj.id,
        "start_date": payload.start_date,
        "end_date": payload.end_date,
        "date_type": payload.date_type
    }

    for key, value in filter_map.items():
        if value is not None:
            param = db.query(CMSMSTParameter).filter(CMSMSTParameter.code == key).first()
            if param:
                param_entry = CMSClientReportParameter(
                    reportId=report.id,
                    parameterId=param.id,
                    value=str(value)
                )
                db.add(param_entry)

    db.commit()
    return {"message": "Report view updated successfully", "report_id": report.id}


# Delete the created reports
@router.delete("/reports/{report_id}", status_code=200)
def delete_report(
    report_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    # Step 1: Fetch the report
    report = db.query(CMSClientReport).filter(
        CMSClientReport.id == report_id,
        CMSClientReport.userId == user_id
    ).first()

    if not report:
        raise HTTPException(status_code=404, detail="Report not found or not authorized to delete")

    # Step 2: Delete related cache entries
    db.query(CMSCache).filter(CMSCache.reportId == report_id).delete()

    # Step 3: Delete related report parameters
    db.query(CMSClientReportParameter).filter(CMSClientReportParameter.reportId == report_id).delete()

    # Step 4: Delete the report
    db.delete(report)
    db.commit()

    return {"message": "Report and related cache data deleted successfully"}

    



