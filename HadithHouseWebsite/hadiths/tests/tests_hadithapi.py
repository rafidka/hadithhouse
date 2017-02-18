from django.test import Client
from rest_framework.status import HTTP_403_FORBIDDEN, HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_201_CREATED, \
  HTTP_204_NO_CONTENT

from hadiths.tests.setup import TestCaseBase


class HadithPostApiTestCase(TestCaseBase):
  def test__post__no_auth_token__403(self):
    resp = self.post('/apis/hadiths', {'text': 'test'})
    self.assertEqual(HTTP_403_FORBIDDEN, resp.status_code)
    self.assertEqual(HTTP_403_FORBIDDEN, resp.data['status_code'])
    self.assertEqual("Couldn't authenticate user.", resp.data['error'])

  def test__post__invalid_auth_token__403(self):
    resp = self.post('/apis/hadiths?fb_token=%s' % TestCaseBase.invalid_accesstoken, {'text': 'test'})
    self.assertEqual(HTTP_403_FORBIDDEN, resp.status_code)
    self.assertEqual(HTTP_403_FORBIDDEN, resp.data['status_code'])
    self.assertEqual("Invalid Facebook access token.", resp.data['error'])

  def test__post__valid_auth_token__no_user_permission__401(self):
    resp = self.post('/apis/hadiths?fb_token=%s' % TestCaseBase.jack_accesstoken, {'text': 'test'})
    self.assertEqual(HTTP_403_FORBIDDEN, resp.status_code)
    self.assertEqual(HTTP_403_FORBIDDEN, resp.data['status_code'])
    self.assertEqual("User doesn't have permission for this action.", resp.data['error'])

  def test__post__valid_auth_token__user_permission__no_text__400(self):
    resp = self.post('/apis/hadiths?fb_token=%s' % TestCaseBase.marie_accesstoken, {})
    self.assertEqual(HTTP_400_BAD_REQUEST, resp.status_code)
    self.assertEqual(HTTP_400_BAD_REQUEST, resp.data['status_code'])
    self.assertEqual("Invalid input.", resp.data['error'])
    self.assertTrue('text' in resp.data['detail'])
    self.assertEqual(['This field is required.'], resp.data['detail']['text'])

  def test__post__valid_auth_token__user_permission__blank_text__400(self):
    resp = self.post('/apis/hadiths?fb_token=%s' % TestCaseBase.marie_accesstoken, {'text': ' '})
    self.assertEqual(HTTP_400_BAD_REQUEST, resp.status_code)
    self.assertEqual(HTTP_400_BAD_REQUEST, resp.data['status_code'])
    self.assertEqual("Invalid input.", resp.data['error'])
    self.assertTrue('text' in resp.data['detail'])
    self.assertEqual(['This field may not be blank.'], resp.data['detail']['text'])

  def test__post__valid_auth_token__user_permission__valid_text__hadith_added(self):
    resp = self.post('/apis/hadiths?fb_token=%s' % TestCaseBase.marie_accesstoken, {'text': 'test', 'tags': []})
    self.assertEqual(HTTP_201_CREATED, resp.status_code)
    hadith = resp.data
    self.assertEqual('test', hadith['text'])

    resp2 = self.get('/apis/hadiths/%d' % hadith['id'])
    self.assertEqual(HTTP_200_OK, resp2.status_code)
    hadith2 = resp2.data

    self.assertEqual(hadith['id'], hadith2['id'])
    self.assertEqual(hadith['text'], hadith2['text'])
    self.assertEqual(hadith['person'], hadith2['person'])
    self.assertEqual(hadith['book'], hadith2['book'])
    self.assertEqual(hadith['volume'], hadith2['volume'])
    self.assertEqual(hadith['chapter'], hadith2['chapter'])
    self.assertEqual(hadith['section'], hadith2['section'])
    self.assertEqual(hadith['number'], hadith2['number'])
    self.assertEqual(hadith['added_on'], hadith2['added_on'])
    self.assertEqual(hadith['added_by'], hadith2['added_by'])
    self.assertEqual(hadith['updated_on'], hadith2['updated_on'])
    self.assertEqual(hadith['updated_by'], hadith2['updated_by'])


class HadithPutApiTestCase(TestCaseBase):
  hadith = None
  hadith_id = None

  @classmethod
  def setUpClass(cls):
    TestCaseBase.setUpClass()
    c = Client()
    resp = c.post('/apis/hadiths?fb_token=%s' % TestCaseBase.marie_accesstoken, {'text': 'test'})
    assert resp.status_code == HTTP_201_CREATED
    cls.hadith = resp.data
    cls.hadith_id = cls.hadith['id']

  @classmethod
  def tearDownClass(cls):
    c = Client()
    resp = c.delete('/apis/hadiths/%d?fb_token=%s' % (HadithPutApiTestCase.hadith_id, TestCaseBase.marie_accesstoken),
                    {'title': 'test'})
    assert resp.status_code == HTTP_204_NO_CONTENT
    TestCaseBase.tearDownClass()

  def test__put__no_auth_token__403(self):
    resp = self.put('/apis/hadiths/%d' % HadithPutApiTestCase.hadith_id, {'text': 'test'})
    self.assertEqual(HTTP_403_FORBIDDEN, resp.status_code)
    self.assertEqual(HTTP_403_FORBIDDEN, resp.data['status_code'])
    self.assertEqual("Couldn't authenticate user.", resp.data['error'])

  def test__put__invalid_auth_token__403(self):
    resp = self.put('/apis/hadiths/%d?fb_token=%s' % (HadithPutApiTestCase.hadith_id, TestCaseBase.invalid_accesstoken),
                    {'text': 'test'})
    self.assertEqual(HTTP_403_FORBIDDEN, resp.status_code)
    self.assertEqual(HTTP_403_FORBIDDEN, resp.data['status_code'])
    self.assertEqual("Invalid Facebook access token.", resp.data['error'])

  def test__put__valid_auth_token__no_user_permission__401(self):
    resp = self.put('/apis/hadiths/%d?fb_token=%s' % (HadithPutApiTestCase.hadith_id, TestCaseBase.jack_accesstoken),
                    {'text': 'test'})
    self.assertEqual(HTTP_403_FORBIDDEN, resp.status_code)
    self.assertEqual(HTTP_403_FORBIDDEN, resp.data['status_code'])
    self.assertEqual("User doesn't have permission for this action.", resp.data['error'])

  def test__put__valid_auth_token__user_permission__no_text__400(self):
    resp = self.put('/apis/hadiths/%d?fb_token=%s' % (HadithPutApiTestCase.hadith_id, TestCaseBase.marie_accesstoken),
                    {})
    self.assertEqual(HTTP_400_BAD_REQUEST, resp.status_code)
    self.assertEqual(HTTP_400_BAD_REQUEST, resp.data['status_code'])
    self.assertEqual("Invalid input.", resp.data['error'])
    self.assertTrue('text' in resp.data['detail'])
    self.assertEqual(['This field is required.'], resp.data['detail']['text'])

  def test__put__valid_auth_token__user_permission__blank_text__400(self):
    resp = self.put('/apis/hadiths/%d?fb_token=%s' % (HadithPutApiTestCase.hadith_id, TestCaseBase.marie_accesstoken),
                    {'text': ' '})
    self.assertEqual(HTTP_400_BAD_REQUEST, resp.status_code)
    self.assertEqual(HTTP_400_BAD_REQUEST, resp.data['status_code'])
    self.assertEqual("Invalid input.", resp.data['error'])
    self.assertTrue('text' in resp.data['detail'])
    self.assertEqual(['This field may not be blank.'], resp.data['detail']['text'])

  def test__put__valid_auth_token__user_permission__valid_text__hadith_updated(self):
    resp = self.put('/apis/hadiths/%d?fb_token=%s' % (HadithPutApiTestCase.hadith_id, TestCaseBase.marie_accesstoken),
                    {'text': 'test_updated', 'tags': []})
    self.assertEqual(HTTP_200_OK, resp.status_code)
    hadith = resp.data
    self.assertEqual('test_updated', hadith['text'])

    resp2 = self.get('/apis/hadiths/%d' % hadith['id'])
    self.assertEqual(HTTP_200_OK, resp2.status_code)
    hadith2 = resp2.data

    self.assertEqual(hadith['id'], hadith2['id'])
    self.assertEqual(hadith['text'], hadith2['text'])
    self.assertEqual(hadith['person'], hadith2['person'])
    self.assertEqual(hadith['book'], hadith2['book'])
    self.assertEqual(hadith['volume'], hadith2['volume'])
    self.assertEqual(hadith['chapter'], hadith2['chapter'])
    self.assertEqual(hadith['section'], hadith2['section'])
    self.assertEqual(hadith['number'], hadith2['number'])
    self.assertEqual(hadith['added_on'], hadith2['added_on'])
    self.assertEqual(hadith['added_by'], hadith2['added_by'])
    self.assertEqual(hadith['updated_on'], hadith2['updated_on'])
    self.assertEqual(hadith['updated_by'], hadith2['updated_by'])


class HadithPatchApiTestCase(TestCaseBase):
  hadith = None
  hadith_id = None

  @classmethod
  def setUpClass(cls):
    TestCaseBase.setUpClass()
    c = Client()
    resp = c.post('/apis/hadiths?fb_token=%s' % TestCaseBase.marie_accesstoken, {'text': 'test'})
    assert resp.status_code == HTTP_201_CREATED
    cls.hadith = resp.data
    cls.hadith_id = cls.hadith['id']

  @classmethod
  def tearDownClass(cls):
    c = Client()
    resp = c.delete('/apis/hadiths/%d?fb_token=%s' % (HadithPatchApiTestCase.hadith_id, TestCaseBase.marie_accesstoken),
                    {'text': 'test'})
    assert resp.status_code == HTTP_204_NO_CONTENT
    TestCaseBase.tearDownClass()

  def test__patch__no_auth_token__403(self):
    resp = self.patch('/apis/hadiths/%d' % HadithPatchApiTestCase.hadith_id, {'text': 'test'})
    self.assertEqual(HTTP_403_FORBIDDEN, resp.status_code)
    self.assertEqual(HTTP_403_FORBIDDEN, resp.data['status_code'])
    self.assertEqual("Couldn't authenticate user.", resp.data['error'])

  def test__patch__invalid_auth_token__403(self):
    resp = self.patch('/apis/hadiths/%d?fb_token=%s' %
                      (HadithPatchApiTestCase.hadith_id, TestCaseBase.invalid_accesstoken), {'text': 'test'})
    self.assertEqual(HTTP_403_FORBIDDEN, resp.status_code)
    self.assertEqual(HTTP_403_FORBIDDEN, resp.data['status_code'])
    self.assertEqual("Invalid Facebook access token.", resp.data['error'])

  def test__patch__valid_auth_token__no_user_permission__401(self):
    resp = self.patch('/apis/hadiths/%d?fb_token=%s' %
                      (HadithPatchApiTestCase.hadith_id, TestCaseBase.jack_accesstoken), {'text': 'test'})
    self.assertEqual(HTTP_403_FORBIDDEN, resp.status_code)
    self.assertEqual(HTTP_403_FORBIDDEN, resp.data['status_code'])
    self.assertEqual("User doesn't have permission for this action.", resp.data['error'])

  def test__patch__valid_auth_token__user_permission__no_title__200(self):
    resp = self.patch('/apis/hadiths/%d?fb_token=%s' %
                      (HadithPatchApiTestCase.hadith_id, TestCaseBase.marie_accesstoken), {})
    self.assertEqual(HTTP_200_OK, resp.status_code)

  def test__patch__valid_auth_token__user_permission__blank_title__400(self):
    resp = self.patch('/apis/hadiths/%d?fb_token=%s' %
                      (HadithPatchApiTestCase.hadith_id, TestCaseBase.marie_accesstoken), {'text': ' '})
    self.assertEqual(HTTP_400_BAD_REQUEST, resp.status_code)
    self.assertEqual(HTTP_400_BAD_REQUEST, resp.data['status_code'])
    self.assertEqual("Invalid input.", resp.data['error'])
    self.assertTrue('text' in resp.data['detail'])
    self.assertEqual(['This field may not be blank.'], resp.data['detail']['text'])

  def test__patch__valid_auth_token__user_permission__valid_title__person_updated(self):
    resp = self.patch('/apis/hadiths/%d?fb_token=%s' %
                      (HadithPatchApiTestCase.hadith_id, TestCaseBase.marie_accesstoken), {'text': 'test_updated'})
    self.assertEqual(HTTP_200_OK, resp.status_code)
    hadith = resp.data
    self.assertEqual('test_updated', hadith['text'])

    resp2 = self.get('/apis/hadiths/%d' % hadith['id'])
    self.assertEqual(HTTP_200_OK, resp2.status_code)
    hadith2 = resp2.data

    self.assertEqual(hadith['id'], hadith2['id'])
    self.assertEqual(hadith['text'], hadith2['text'])
    self.assertEqual(hadith['person'], hadith2['person'])
    self.assertEqual(hadith['book'], hadith2['book'])
    self.assertEqual(hadith['volume'], hadith2['volume'])
    self.assertEqual(hadith['chapter'], hadith2['chapter'])
    self.assertEqual(hadith['section'], hadith2['section'])
    self.assertEqual(hadith['number'], hadith2['number'])
    self.assertEqual(hadith['added_on'], hadith2['added_on'])
    self.assertEqual(hadith['added_by'], hadith2['added_by'])
    self.assertEqual(hadith['updated_on'], hadith2['updated_on'])
    self.assertEqual(hadith['updated_by'], hadith2['updated_by'])
